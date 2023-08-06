# -*- coding: utf-8 -*-
"""Setup configuration."""

from setuptools import find_packages
from setuptools import setup

setup(
    name="curibio.sdk",
    version="0.11.0",
    description="CREATE A DESCRIPTION",
    url="https://github.com/CuriBio/curibio.sdk",
    project_urls={"Documentation": "https://curibiosdk.readthedocs.io/en/latest/"},
    author="Curi Bio",
    author_email="contact@curibio.com",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages("src"),
    namespace_packages=["curibio"],
    install_requires=[
        "h5py>=3.1.0",
        "nptyping>=1.4.0",
        "numpy>=1.20.1",
        "immutabledict>=1.2.0",
        "XlsxWriter>=1.3.7",
        "openpyxl>=3.0.6",
        "matplotlib>=3.3.4",
        "mantarray-file-manager>=0.4.6",
        "stdlib_utils>=0.4.2",
        "mantarray-waveform-analysis>=0.6.0",
        "labware-domain-models>=0.3.1",
        "requests>=2.25.1",
        'importlib-metadata ~= 1.0 ; python_version < "3.8"',
    ],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
    ],
)
