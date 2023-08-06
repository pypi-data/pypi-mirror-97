import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-aws-secure",
    "version": "1.0.2",
    "description": "High level CDKTF construct to provision secure configurations with AWS",
    "license": "Apache-2.0",
    "url": "https://github.com/shazi7804/cdktf-aws-secure-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Scott Liao<shazi7804@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/shazi7804/cdktf-aws-secure-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_aws_secure",
        "cdktf_aws_secure._jsii"
    ],
    "package_data": {
        "cdktf_aws_secure._jsii": [
            "cdktf-aws-secure@1.0.2.jsii.tgz"
        ],
        "cdktf_aws_secure": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "cdktf-cdktf-provider-aws>=1.0.17, <2.0.0",
        "cdktf>=0.1.0, <0.2.0",
        "constructs>=3.0.0, <4.0.0",
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
