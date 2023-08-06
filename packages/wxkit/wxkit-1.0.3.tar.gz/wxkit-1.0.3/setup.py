#!/usr/bin/env python3

import sys
import re
from setuptools import setup, find_packages

DESC_PATTERN = re.compile(r"(# ){1}[\S]+([\s\w\.\?\!-_]+)(## ){1}.*")

if sys.version_info.major < 3:
    sys.exit("Sorry, Python2.x is not supported")

with open("README.md", encoding="UTF-8") as readme_file:
    readme = readme_file.read()
    _m = DESC_PATTERN.match(readme)
    assert _m, "Description is not matched"
    description = description = _m.group(2).strip()

with open("LICENSE", encoding="UTF-8") as license_file:
    license = license_file.read()


requirements = list()
with open("requirements.txt", "r") as fp:
    install_reqs = fp.readlines()
    requirements = [ir.rstrip() for ir in install_reqs if not ir.startswith("-")]

test_requirements = ["pytest", "tox"]

setup(
    name="wxkit",
    version="1.0.3",
    description=description,
    long_description=readme,
    url="https://github.com/returnchung/wxkit",
    author="JuiTeng Chung",
    author_email="return1225@gmail.com",
    license=license,
    python_requires=">=3",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X"
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
    ],
    packages=find_packages(include=["wxkit*"]),
    install_requires=requirements,
    test_suite="tests",
    tests_require=test_requirements,
    keywords="weather, wx, openweather",
    zip_safe=False,
)
