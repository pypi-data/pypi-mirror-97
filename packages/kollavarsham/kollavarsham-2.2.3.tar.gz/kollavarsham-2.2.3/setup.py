import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "kollavarsham",
    "version": "2.2.3",
    "description": "Convert Gregorian date to Kollavarsham date and vice versa",
    "license": "MIT",
    "url": "http://kollavarsham.org",
    "long_description_content_type": "text/markdown",
    "author": "The Kollavarsham Team<info@kollavarsham.org>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/kollavarsham/kollavarsham-js.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "kollavarsham",
        "kollavarsham._jsii"
    ],
    "package_data": {
        "kollavarsham._jsii": [
            "kollavarsham@2.2.3.jsii.tgz"
        ],
        "kollavarsham": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
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
