import boto3
import botocore.session
import logging
from logging import NullHandler
from boto3_extensions.arn_patch import (
    patch_session,
    patch_service_context,
    patch_resource_factory,
    patch_resource_meta,
    patch_create_request_parameters,
)
from os import environ, path
from imp import reload

logging.getLogger(__name__).addHandler(NullHandler())
_logger = logging.getLogger(__name__)

dir_path = path.dirname(path.realpath(__file__))
environ["AWS_DATA_PATH"] = "{dir_path}/data/".format(dir_path=dir_path)
reload(boto3)


def arn_patch_boto3():
    """
    Patch boto3 to support ARNs for all resources
    """
    patch_session()
    patch_service_context()
    patch_resource_factory()
    patch_resource_meta()
    patch_create_request_parameters()
    _logger.info("Patched Boto3 with arn support")


class _CredentialSourcer:
    TYPE = "boto3_extensions"

    def __init__(self, base_session):
        if not base_session:
            base_session = boto3.Session()
        self._base_session = base_session

    def is_supported(self, source):
        return source == self.TYPE

    def source_credentials(self, *args, **kwargs):
        return self._base_session.get_credentials()


def get_role_session(role_arn, role_session_name=None, base_session=None, **kwargs):
    botocore_session = botocore.session.Session()
    botocore_session.full_config["profiles"][role_arn] = {
        "role_arn": role_arn,
        "credential_source": _CredentialSourcer.TYPE,
        "session_name": role_session_name,
    }
    if "external_id" in kwargs:
        botocore_session.full_config["profiles"][role_arn]["external_id"] = kwargs.pop("external_id")

    session = boto3.Session(profile_name=role_arn, botocore_session=botocore_session, **kwargs)

    session._session.get_component("credential_provider").get_provider(
        "assume-role"
    )._credential_sourcer = _CredentialSourcer(base_session)

    return session


class ConnectionManager:
    """
    Usage:
        connections = ConnectionManager(region_name='us-east-1')
        session = connections.get_session(role_arn='arn:aws:iam::1234567890:role/test-role', role_session_name='test')

    You can also provide a base session if you prefer:
        connections = ConnectionManager(session=my_boto3_session)

    """

    def __init__(self, session=None, **kwargs):
        self._base_session = session
        self.default_session_args = kwargs
        self.cache = Cache()

    def get_session(self, role_arn, role_session_name, external_id=None, skip_cache=False, force_cache_refresh=False):
        args = self.default_session_args
        if external_id:
            args["external_id"] = external_id

        if skip_cache:
            return get_role_session(role_arn, role_session_name, self._base_session, **args)

        session = None
        if not force_cache_refresh:
            session = self.cache.get(role_arn, role_session_name)

        if not session:
            _logger.debug(f"Session cache miss for {role_arn}/{role_session_name}.")
            session = get_role_session(role_arn, role_session_name, self._base_session, **args)
            _logger.debug(f"Session cache saved for {role_arn}/{role_session_name}.")
            self.cache.set(role_arn, role_session_name, session)
        else:
            _logger.debug(f"Session cache hit for {role_arn}/{role_session_name}.")
        return session


class Cache:
    """Cache class.

    Implements a very basic Session caching system. The main use-case for this class is for it to be monkey-patched
    by the calling application to use whichever caching mechanism is appropriate.
    """

    def __init__(self):
        self._cache = {}

    def get(self, role_arn, role_session_name):
        """Retrieve an existing Session from the cache.

        :param role_arn: ARN of the Role to be assumed.
        :type role_arn: str
        :param role_session_name: Unique name for the Session.
        :type role_session_name: str
        :return: Boto3 Session object or None if cache miss.
        :rtype: boto3.Session | None
        """
        return self._cache.get((role_arn, role_session_name), None)

    def set(self, role_arn, role_session_name, session):
        """Add a Session object to the cache.

        :param role_arn: ARN of the Role to be assumed.
        :type role_arn: str
        :param role_session_name: Unique name for the Session.
        :type role_session_name: str
        :param session: Existing Boto3 Session object.
        :type session: boto3.Session
        """
        self._cache[(role_arn, role_session_name)] = session