import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "ses-email-forwarding",
    "version": "3.0.3",
    "description": "@seeebiii/ses-email-forwarding",
    "license": "MIT",
    "url": "https://github.com/seeebiii/ses-email-forwarding",
    "long_description_content_type": "text/markdown",
    "author": "Sebastian Hesse<info@sebastianhesse.de>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/seeebiii/ses-email-forwarding"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "ses_email_forwarding",
        "ses_email_forwarding._jsii"
    ],
    "package_data": {
        "ses_email_forwarding._jsii": [
            "ses-email-forwarding@3.0.3.jsii.tgz"
        ],
        "ses_email_forwarding": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-iam==1.91.0",
        "aws-cdk.aws-lambda-nodejs==1.91.0",
        "aws-cdk.aws-lambda==1.91.0",
        "aws-cdk.aws-logs==1.91.0",
        "aws-cdk.aws-s3==1.91.0",
        "aws-cdk.aws-ses-actions==1.91.0",
        "aws-cdk.aws-ses==1.91.0",
        "aws-cdk.aws-sns==1.91.0",
        "aws-cdk.aws-ssm==1.91.0",
        "aws-cdk.core==1.91.0",
        "aws-cdk.custom-resources==1.91.0",
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
