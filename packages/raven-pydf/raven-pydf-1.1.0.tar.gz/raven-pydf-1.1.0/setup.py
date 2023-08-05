# Copyright 2021 Raven Computing
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""An implementation of the DataFrame specification in Python."""

import os

from setuptools import setup, find_namespace_packages

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(PROJECT_ROOT, "README.md")) as f:
    README = f.read()

setup(
    name="raven-pydf",
    version="1.1.0",
    description="An implementation of the DataFrame specification in Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/raven-computing/pydf",
    author="Phil Gaiser",
    author_email="phil.gaiser@raven-computing.com",
    license="Apache Software License",
    packages=find_namespace_packages(include=("raven.*",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0"
    ],
)
