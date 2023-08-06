import re

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("shirkhan/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="shirkhan",
    version=version,
    author="shirkhan",
    author_email="uybabbage@hotmail.com",
    description="shirkhan tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ishirkhan",
    packages=find_packages(),
    install_requires=[
        "pycryptodome"
    ],

    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
