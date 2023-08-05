# coding: utf-8
# Copyright (c) Materials Virtual Lab
# Distributed under the terms of the BSD License.

from setuptools import setup, find_namespace_packages

long_desc = """
This is the package associated with our recent publication:

Zheng, C., Chen, C., Chen, Y.M. & Ong, S.P. (2020), Random Forest Models for Accurate Identification of Coordination
Environments from X-ray Absorption Near-Edge Structure, Patterns, accepted.
Usage example of the package can be found in the notebooks folder and experiment.csv contains processed experimental
data used in the paper.

Installation
------------

Pip install via PyPI::

    pip install maml-apps-rfxas
"""

setup(
    name="maml-apps-rfxas",
    namespace_packages=['maml.apps'],
    packages=find_namespace_packages(include=['maml.apps.*']),
    version="2021.3.2",
    install_requires=["numpy", "scipy", "monty", "scikit-learn", "pandas", "pymatgen", "tqdm"],
    author="Materials Virtual Lab",
    author_email="ongsp@eng.ucsd.edu",
    maintainer="Shyue Ping Ong",
    maintainer_email="ongsp@eng.ucsd.edu",
    url="http://maml.ai/",
    license="BSD",
    description="maml-apps-rfxas is a maml add-on to perform RF analysis of X-ray Absorption Spectra.",
    long_description=long_desc,
    keywords=["materials", "science", "deep", "learning"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    include_package_data=True,

)
