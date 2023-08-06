#!/usr/bin/env python
"""
Install wagtailpolls using setuptools
"""

from setuptools import find_packages, setup

from wagtailpolls import __version__

with open("README.rst", "r") as f:
    readme = f.read()

setup(
    name="wagtailpolls-ng",
    version=__version__,
    description="A polling plugin for the Wagtail CMS",
    long_description=readme,
    author="Takeflight",
    author_email="liam@takeflight.com.au",
    url="https://github.com/frague59/wagtailpolls",
    install_requires=[
        "wagtail>=2.5",
        "django-ipware",
        "django",
    ],
    zip_safe=False,
    license="BSD License",
    packages=find_packages(),
    include_package_data=True,
    package_data={},
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "License :: OSI Approved :: BSD License",
    ],
)
