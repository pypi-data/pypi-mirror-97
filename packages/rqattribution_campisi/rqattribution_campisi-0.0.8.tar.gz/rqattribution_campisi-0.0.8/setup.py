# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="rqattribution_campisi",
    version="0.0.8",
    description="campisi model performance attribution",
    author="Ricequant",
    author_email="public@ricequant.com",
    keywords="rqattribution",
    url="https://www.ricequant.com/",
    include_package_data=True,
    packages=find_packages(include=["rqattribution_campisi", "rqattribution_campisi.*"]),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    zip_safe=False,
)
