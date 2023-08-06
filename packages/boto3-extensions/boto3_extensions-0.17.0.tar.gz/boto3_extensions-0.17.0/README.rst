================
Boto3 Extensions
================

Overview
--------
This module adds more resource files to the Boto3 library and includes some functionality enhancements.

Quick Start
-----------
First, install the library:

.. code-block:: sh

    $ pip install boto3_extensions

Follow the Boto3 docs on setting up your region and credentials (https://github.com/boto/boto3).

Then, from a Python interpreter:

.. code-block:: python

    >>> import boto3
    >>> import boto3_extensions
    >>> r = boto3.resource('cloudtrail', region_name='us-east-1')
    >>> for trail in r.trails.all():
          print(trail.trail_arn)

Resource Files
--------------
The following resource files are **added** to the Boto3 library.

  * acm
  * autoscaling
  * cloudfront
  * cloudtrail
  * cur
  * datapipeline
  * directconnect
  * elasticache
  * elb
  * elbv2
  * emr
  * glue
  * health
  * kinesis
  * lambda
  * rds
  * redshift
  * route53
  * support

The following resource files are **updated** in the Boto3 library.

  * dynamodb
  * ec2
  * iam
  * s3


RefreshableAssumeRoleProvider
-----------------------------
If your code needs to AssumeRole into another role before performing actions against the AWS API (be it in the same or another AWS account), you run the risk that the credentials you are using expire during their use. You can either add code to your application to constantly check the credential expiry time or using this extension offload the credential refresh to boto3 itself. By using the ConnectionManager in boto3_extensions not only will it automattically assumeRole when the credentials get below 15 mins left, but it will also cache the credentials. This means that if your application is calling boto3 to get credentials for another role more than once the ConnectionManager will cache the first call and then hand out the same session for the subsequent calls. 

.. code-block:: python

    >>> role_arn = 'arn:aws:iam::1234567890:role/test-role'
    >>> role_session_name = 'test'
    >>> connections = boto3_extensions.ConnectionManager(region_name='us-east-1')
    >>> session = connections.get_session(role_arn=role_arn, role_session_name=role_session_name)
    >>>
    >>> r = session.resource('cloudtrail', region_name='us-east-1')
    >>> for trail in r.trails.all():
    >>>     print(trail.trail_arn)


ARN Patch
---------
It would be nice to have a consistent way to get the ARN of resources. The ARN patch feature of boto3_extensions allows you to get the arn from resources via an arn attribute. 

.. code-block:: python

    >>> import boto3
    >>> import boto3_extensions
    >>> from imp import reload
    >>> boto3_extensions.arn_patch_boto3()
    >>> reload(boto3)
    >>> 
    >>> r = boto3.resource('rds', region_name='us-east-1')
    >>> for db in r.db_instances.all():
    >>>   print(db.arn)


Session Caching
------------------
There is basic Session caching builtin that simply stores the :code:`Session` for a each assumed Role into a dict, but if you require another caching mechanism you can monkey patch the :code:`boto3_extensions.Cache` class, as long as you supply the :code:`Cache.get()` and :code:`Cache.set()` methods.

.. code-block:: python

    >>> import boto3
    >>> import boto3_extensions
    >>> from boto3_extensions import ConnectionManager
    >>> class MyCache:
            def __init__(self):
                self._cache = {}

            def get(self, role_arn, role_session_name):
                print("inside MyCache.get()")
                return self._cache.get((role_arn, role_session_name), None)

            def set(self, role_arn, role_session_name, session):
                print("inside MyCache.set()")
                self._cache[(role_arn, role_session_name)] = session
    >>> boto3_extensions.Cache = MyCache
    >>> connections = ConnectionManager()
    >>> connections.get_session(role_arn="arn:aws:iam::012345678912:role/test_role", role_session_name="testing")
        inside MyCache.get()
        inside MyCache.set()
    >>> connections.get_session(role_arn="arn:aws:iam::012345678912:role/test_role", role_session_name="testing")
        inside MyCache.get()

In the above we monkey patch the :code:`Cache` class and call :code:`get_session()` twice. The output shows that the first time we have a cache get which results in a cache miss and thena cache set after the credential is retrieved from STS. We then run :code:`get_session()` a second time and as the :code:`Session` is now cached we only see a cache get resulting in a cache hit.

Getting Help
------------
Please raise issue ticket inside our Bitbucket repo: https://bitbucket.org/atlassian/boto3_extensions/issues
