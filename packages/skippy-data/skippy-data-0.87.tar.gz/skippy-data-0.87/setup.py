import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skippy-data",
    version="0.87",
    author="Cynthia Marcelino",
    author_email="keniack@gmail.com",
    description="look up data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.dsg.tuwien.ac.at/c.marcelino/skippy-data",
    download_url="https://git.dsg.tuwien.ac.at/c.marcelino/skippy-data",
    packages=setuptools.find_packages(),
    setup_requires=['wheel'],
    install_requires=['kubernetes~=12.0.1','minio~=5.0.10','redis~=3.5.3','PyYAML~=5.3.1'],
    pyton_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
