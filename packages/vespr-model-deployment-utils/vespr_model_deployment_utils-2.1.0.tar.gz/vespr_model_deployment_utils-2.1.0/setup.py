"""setup."""
import os

from setuptools import find_packages, setup

if os.path.isfile("VERSION"):
    with open("VERSION") as version:
        __version__ = version.read().strip("v")
else:
    __version__ = "0.0.0"

with open("README.md", "r") as fh:
    long_description = fh.read() or ""


setup(
    name="vespr_model_deployment_utils",
    version=__version__,
    author="Calypso AI",
    description="VESPR Data Processing Utilities Package",
    long_description=long_description,
    packages=find_packages(),
    url="https://gitlab.com/CalypsoAI/vespr-model-deployment-utils",
    install_requires=[
        "numpy>=1.18.1",
        "pandas>=1.0.1",
        "scikit-learn==0.23.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
