#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import pathlib

from setuptools import find_packages
from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()
# Get the long description from the README file
long_description = (here / "pypidesc.md").read_text(encoding="utf-8")
setup(
    version="1.1.0",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "click",
        "certifi",
        "delphixpy",
        "python-dateutil",
        "colorama",
        "tabulate",
        "cryptography",
    ],
    # Format is mypkg.mymodule:the_function'
    entry_points="""
        [console_scripts]
        dxi=dxi._cli._dxi:dxi
    """,
    author="Delphix Engineering",
    keywords="dxi, delphix, delphix integration, delphix automation",  # noqa
    license="Apache 2",
    description=("Delphix Integration Library and CLI"),
    dependency_links=[],
    name="dxi",  #
    long_description_content_type="text/markdown",
    long_description=long_description,
    include_package_data=True,
    project_urls={},  # Optional
)
