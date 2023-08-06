import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-appsync-transformer",
    "version": "1.77.10",
    "description": "cdk-appsync-transformer",
    "license": "Apache-2.0",
    "url": "https://github.com/kcwinner/cdk-appsync-transformer.git",
    "long_description_content_type": "text/markdown",
    "author": "Ken Winner<kcswinner@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/kcwinner/cdk-appsync-transformer.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_appsync_transformer",
        "cdk_appsync_transformer._jsii"
    ],
    "package_data": {
        "cdk_appsync_transformer._jsii": [
            "cdk-appsync-transformer@1.77.10.jsii.tgz"
        ],
        "cdk_appsync_transformer": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-appsync>=1.77.0, <2.0.0",
        "aws-cdk.aws-cognito>=1.77.0, <2.0.0",
        "aws-cdk.aws-dynamodb>=1.77.0, <2.0.0",
        "aws-cdk.aws-iam>=1.77.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.77.0, <2.0.0",
        "aws-cdk.core>=1.77.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.21.0, <2.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
