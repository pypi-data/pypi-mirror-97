#
#  Pysocket Template
#  Template classes for Python socket applications.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-socket",
    version="0.0.2",
    author="Patrick Huang",
    author_email="huangpatrick16777216@gmail.com",
    description="Template classes for Python socket applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HuangPatrick16777216/pysocket",
    py_modules=["pysocket"],
    packages=setuptools.find_packages(),
    install_requires=[
        "cryptography",
        "bcon",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
)
