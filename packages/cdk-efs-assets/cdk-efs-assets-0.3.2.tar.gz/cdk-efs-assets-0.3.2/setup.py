import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-efs-assets",
    "version": "0.3.2",
    "description": "Amazon EFS assets from Github repositories or S3 buckets",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/cdk-efs-assets.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<pahudnet@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pahud/cdk-efs-assets.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_efs_assets",
        "cdk_efs_assets._jsii"
    ],
    "package_data": {
        "cdk_efs_assets._jsii": [
            "cdk-efs-assets@0.3.2.jsii.tgz"
        ],
        "cdk_efs_assets": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-ec2>=1.83.0, <2.0.0",
        "aws-cdk.aws-ecs>=1.83.0, <2.0.0",
        "aws-cdk.aws-efs>=1.83.0, <2.0.0",
        "aws-cdk.aws-events-targets>=1.83.0, <2.0.0",
        "aws-cdk.aws-iam>=1.83.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.83.0, <2.0.0",
        "aws-cdk.aws-logs>=1.83.0, <2.0.0",
        "aws-cdk.aws-s3>=1.83.0, <2.0.0",
        "aws-cdk.aws-secretsmanager>=1.83.0, <2.0.0",
        "aws-cdk.core>=1.83.0, <2.0.0",
        "aws-cdk.custom-resources>=1.83.0, <2.0.0",
        "cdk-fargate-run-task>=0.0.65, <0.0.66",
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
