# File: setup.py
# Date: 8-Mar-2020
#
# Update:

#
import re

from setuptools import find_packages
from setuptools import setup

packages = []
thisPackage = "rcsb.app.chem"

with open("rcsb/app/chem/__init__.py", "r") as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

setup(
    name=thisPackage,
    version=version,
    description="RCSB Chemical Search Service",
    long_description="See:  README.md",
    author="John Westbrook",
    author_email="john.westbrook@rcsb.org",
    url="https://github.com/rcsb/py-rcsb_app_chem",
    #
    license="Apache 2.0",
    classifiers=(
        "Development Status :: 3 - Alpha",
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ),
    entry_points={"console_scripts": []},
    #
    install_requires=[
        "fastapi == 0.63.0",
        "pydantic == 1.7.3",
        "aiofiles >=0.5.0,<=0.6.0",
        "gunicorn == 20.0.4",
        "rcsb.utils.io >= 1.00",
        "rcsb.utils.chem >= 0.62",
        "requests >=2.24.0,<3.0.0",
        "jinja2 >=2.11.2,<3.0.0",
        "python-multipart >=0.0.5,<0.0.6",
        "ujson >=3.0.0,<4.0.0",
        "uvicorn[standard] >=0.12.0,<0.14.0",
        "async_exit_stack >=1.0.1,<2.0.0",
        "async_generator >=1.10,<2.0.0",
    ],
    packages=find_packages(exclude=["rcsb.app.tests-*", "tests.*"]),
    package_data={
        # If any package contains *.md or *.rst ...  files, include them:
        "": ["*.md", "*.rst", "*.txt", "*.cfg"]
    },
    #
    test_suite="rcsb.app.tests-chem",
    tests_require=["tox"],
    #
    # Not configured ...
    extras_require={"dev": ["check-manifest"], "test": ["coverage"]},
    # Added for
    command_options={"build_sphinx": {"project": ("setup.py", thisPackage), "version": ("setup.py", version), "release": ("setup.py", version)}},
    # This setting for namespace package support -
    zip_safe=False,
)
