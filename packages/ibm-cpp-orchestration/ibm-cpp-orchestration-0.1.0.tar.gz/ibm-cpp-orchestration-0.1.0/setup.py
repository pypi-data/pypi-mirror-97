# Copyright IBM Corp. 2020. All Rights Reserved.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
with open('requirements.txt', 'r') as fh:
    for line in fh:
        requirements.append(line.strip())

setuptools.setup(
    name="ibm-cpp-orchestration",
    version="0.1.0",
    author="Michalina Kotwica",
    author_email="michalina.kotwica@ibm.com",
    description="Supports users in usage of CPD Orchestration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.ibm.com/AILifecycle/ibm-cpp-orchestration",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires = requirements,
    package_data={'': [
        'LICENSE',
        'README.md',
        'CONTRIBUTING.md',
        'requirements.txt',
    ]},
    include_package_data=True,
)
