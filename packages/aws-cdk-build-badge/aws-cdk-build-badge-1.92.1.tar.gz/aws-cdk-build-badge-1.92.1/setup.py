import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk-build-badge",
    "version": "1.92.1",
    "description": "aws-cdk-build-badge",
    "license": "Apache-2.0",
    "url": "https://github.com/mmuller88/aws-cdk-build-badge",
    "long_description_content_type": "text/markdown",
    "author": "martin.mueller<damadden88@googlemail.de>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mmuller88/aws-cdk-build-badge"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk_build_badge",
        "aws_cdk_build_badge._jsii"
    ],
    "package_data": {
        "aws_cdk_build_badge._jsii": [
            "aws-cdk-build-badge@1.92.1.jsii.tgz"
        ],
        "aws_cdk_build_badge": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-apigateway==1.92.0",
        "aws-cdk.aws-iam==1.92.0",
        "aws-cdk.aws-lambda-nodejs==1.92.0",
        "aws-cdk.aws-lambda==1.92.0",
        "aws-cdk.core==1.92.0",
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
