import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-s3-bucketreplication",
    "version": "0.0.7",
    "description": "cdk-s3-bucketreplication",
    "license": "Apache-2.0",
    "url": "https://github.com/rogerchi/cdk-s3-bucketreplication.git",
    "long_description_content_type": "text/markdown",
    "author": "Roger Chi<roger@rogerchi.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/rogerchi/cdk-s3-bucketreplication.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_s3_bucketreplication",
        "cdk_s3_bucketreplication._jsii"
    ],
    "package_data": {
        "cdk_s3_bucketreplication._jsii": [
            "cdk-s3-bucketreplication@0.0.7.jsii.tgz"
        ],
        "cdk_s3_bucketreplication": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-iam>=1.92.0, <2.0.0",
        "aws-cdk.aws-s3>=1.92.0, <2.0.0",
        "aws-cdk.core>=1.92.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.24.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
