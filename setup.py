#!/usr/bin/env python3
from setuptools import setup, find_packages
import os
import re

# Read the __version__ from __init__.py
with open("llm_precommit/__init__.py", "r", encoding="utf-8") as f:
    version_match = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", f.read())
    version = version_match.group(1) if version_match else "0.1.0"

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="llm-precommit",
    version=version,
    description="Pre-commit hook using LLM (Gemini) to check code quality and conventions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nguyen Hoang Dang",
    author_email="dang.nh0407@gmail.com",
    url="https://github.com/dang-nh/llm-precommit",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "llm-precommit=llm_precommit.cli:main",
        ],
    },
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
) 