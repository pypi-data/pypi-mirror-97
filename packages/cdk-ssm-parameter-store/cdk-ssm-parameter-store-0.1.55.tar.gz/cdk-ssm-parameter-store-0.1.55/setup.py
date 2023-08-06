import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-ssm-parameter-store",
    "version": "0.1.55",
    "description": "AWS CDK construct that allows you to get the latest Version of the AWS SSM Parameters",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/cdk-ssm-parameter-store.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<pahudnet@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pahud/cdk-ssm-parameter-store.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_ssm_parameter_store",
        "cdk_ssm_parameter_store._jsii"
    ],
    "package_data": {
        "cdk_ssm_parameter_store._jsii": [
            "cdk-ssm-parameter-store@0.1.55.jsii.tgz"
        ],
        "cdk_ssm_parameter_store": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-iam>=1.82.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.82.0, <2.0.0",
        "aws-cdk.aws-ssm>=1.82.0, <2.0.0",
        "aws-cdk.core>=1.82.0, <2.0.0",
        "aws-cdk.custom-resources>=1.82.0, <2.0.0",
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
