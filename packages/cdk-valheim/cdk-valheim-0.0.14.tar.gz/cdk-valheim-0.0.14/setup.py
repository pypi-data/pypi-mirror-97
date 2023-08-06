import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-valheim",
    "version": "0.0.14",
    "description": "cdk-valheim",
    "license": "Apache-2.0",
    "url": "https://github.com/gotodeploy/cdk-valheim.git",
    "long_description_content_type": "text/markdown",
    "author": "gotodeploy<1491134+gotodeploy@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/gotodeploy/cdk-valheim.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_valheim",
        "cdk_valheim._jsii"
    ],
    "package_data": {
        "cdk_valheim._jsii": [
            "cdk-valheim@0.0.14.jsii.tgz"
        ],
        "cdk_valheim": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-applicationautoscaling>=1.91.0, <2.0.0",
        "aws-cdk.aws-backup>=1.91.0, <2.0.0",
        "aws-cdk.aws-ec2>=1.91.0, <2.0.0",
        "aws-cdk.aws-ecs>=1.91.0, <2.0.0",
        "aws-cdk.aws-efs>=1.91.0, <2.0.0",
        "aws-cdk.aws-events>=1.91.0, <2.0.0",
        "aws-cdk.aws-logs>=1.91.0, <2.0.0",
        "aws-cdk.core>=1.91.0, <2.0.0",
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
