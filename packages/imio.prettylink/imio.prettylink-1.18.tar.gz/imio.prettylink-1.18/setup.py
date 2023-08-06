# -*- coding: utf-8 -*-
"""Installer for the imio.prettylink package."""

from setuptools import find_packages
from setuptools import setup


long_description = open("README.rst").read() + "\n" + open("CHANGES.rst").read() + "\n"


setup(
    name="imio.prettylink",
    version='1.18',
    description="Manage generation of a pretty link to an element including coloration, leading icons, ...",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords="plone pretty link utils dev imio",
    author="Gauthier Bastien",
    author_email="gauthier.bastien@imio.be",
    url="http://pypi.python.org/pypi/imio.prettylink",
    license="GPL",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["imio"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "plone.api",
        "setuptools",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.robotframework",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
