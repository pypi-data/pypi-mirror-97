[![Build status](https://gitlab.kwant-project.org/pulkin/miniff/badges/master/pipeline.svg)](https://gitlab.kwant-project.org/pulkin/miniff/pipelines)

miniff: a minimal implementation of neural-network force fields
===============================================================

Compute energies and forces of atomic systems with neural networks.

![image](images/atomic-structure.svg)

About
-----

This package implements [Behler and Parrinello](https://doi.org/10.1103/PhysRevLett.98.146401) approach to simulating
structures and dynamics of atomic systems. You may want to use it if:

- you are interested in structural properties of a system with many atoms such as a molecule or an amorphous material;
- your system is too large for electronic structure treatment (e.g. density functional theory molecular dynamics);
- no empiric potentials for your system exist ...
- ... or the existing empiric potentials are not sufficient to reach the desired tolerances in energies and forces;
- you are interested in machine learning techniques for materials science problems and are looking for a good starting point for your research.

The package is written in Python3.

Built with
----------

- [pytorch](https://pytorch.org/) is the machine learning and autodiff driver for this package;
- [cython](https://cython.org/) is used for performance-critical tasks such as computing descriptors and their
  gradients;
- [numpy](https://numpy.org) is the tensor and data engine in addition to `torch`;
- [scipy](https://www.scipy.org/) is used for sparse data, neighbor search and optimization.

In addition,

- [matplotlib](https://matplotlib.org) is used for plotting, and
- [numericalunits](https://github.com/sbyrnes321/numericalunits) is used for handling units.


Documentation
-------------

Hosted on [Read the Docs](https://miniff.readthedocs.io/en/latest/).

Installation
------------

### Setup prerequisites

* Python3
* C compiler: Required for compiling Cython extensions

Examples 

- Debian Linux
  ```bash
  apt-get install -y build-essential python3-dev python3-pip
  ```
- Fedora
  ```bash
  dnf groupinstall "Development tools" "Development libraries"
  ```
- MacOS:

  Install `gcc` and make sure it is used by default.
  ```bash
  brew install gcc
  ```
  Add to `.bash_profile` path and alias:
  ```bash
  export CC=/usr/local/bin/gcc-10
  alias gcc='gcc-10'
  ```
- Windows:

  On Windows, the support for installing a C compiler and compiling cython extensions is cumbersome and outdated
  as can be inferred from the [Cython Wiki](https://github.com/cython/cython/wiki/CythonExtensionsOnWindows).
  We suggest to use the Windows subsystem for Linux (WSL) in this case.
  More information on WSL and its installation instructions are [here](https://docs.microsoft.com/en-us/windows/wsl/install-win10).


### Installation 

Install via pip

```
pip install miniff
```

Contributing
------------

See CONTRIBUTING.md for contirbution guidelines

Authors
-------

See AUTHORS.MD for the list of contributors

License
-------

This work is licensed under the BSD 2-Clause License
