from setuptools import setup
from setuptools import find_packages

long_description = open("README.rst").read()

VERSION = "0.17.0"
requires = ["boto3>=1.17.24", "botocore>=1.20.24"]

setup(
    name="boto3_extensions",
    version=VERSION,
    description="Extensions to the AWS SDK for Python",
    long_description=long_description,
    url="https://bitbucket.org/atlassian/boto3_extensions/",
    author="Atlassian",
    license="Apache License 2.0",
    install_requires=requires,
    tests_require=["pytest >= 2.5.2"],
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    classifiers=["Programming Language :: Python"],
)
