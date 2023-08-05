#!/usr/bin/env python
import codecs
import re
from os import path

from setuptools import find_packages, setup


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding="utf-8").read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")


setup(
    name="sphinxcontrib-django2",
    version=find_version("sphinxcontrib_django2", "__init__.py"),
    license="Apache 2.0",
    description="Improve the Sphinx autodoc for Django classes.",
    long_description=read("README.rst"),
    author="Timo Ludwig",
    author_email="ti.ludwig@web.de",
    url="https://github.com/timoludwig/sphinxcontrib-django2",
    download_url="https://github.com/timoludwig/sphinxcontrib-django2/zipball/main",
    packages=find_packages(exclude=("example*",)),
    install_requires=[
        "Django>=2.2",
        "Sphinx>=0.5",
        "pprintpp",
    ],
    extras_require={
        "dev": [
            "pre-commit",
        ],
        "test": [
            "pytest",
            "requests-mock",
            "codecov",
        ],
        "doc": [
            "sphinx-rtd-theme",
            "sphinx-last-updated-by-git",
        ],
        "optional": [
            "psycopg2-binary",
            "django-mptt",
            "django-phonenumber-field[phonenumbers]",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
