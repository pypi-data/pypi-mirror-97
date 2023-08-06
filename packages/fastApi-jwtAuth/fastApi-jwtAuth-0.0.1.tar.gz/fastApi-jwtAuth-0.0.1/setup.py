import os
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = "fastApi-jwtAuth",
    version = "0.0.1",
    author = "MohammadAmin Parvanian",
    author_email = "amin_prvn@outlook.com",
    description = ("JWT authentication package for FastAPI framework."),
    license = "Apache License 2.0",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=setuptools.find_packages(),
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires='>=3',
)