Contributions are most welcome and much appreciated! This document will guide you through how to contribute to miniff and will get you up and running towards making your first contribution.

## How to Contribute

Contributions can be made via issues and Merge requests. The [issue list](https://gitlab.kwant-project.org/qt/miniff/-/issues) is the starting point for contributing to miniff. Below are the various ways in which you can contribute.

- Submitting bug reports - Bugs can be reported by opening an issue on the issue list. Please provide the following information when submitting a bug report. 
  - Operating system 
  - Steps to reproduce the issue
  - Any other relevant information that might be helpful
- Bug fixes - Issues with the `bug` label on the issue list are the starting point.
- New features - The issue list captures open work items and ideas that can be picked to work on. You can also suggest new features by opening new issues. 
- Documentation - See [Contributing to documentation](#Contributing-to-documentation) section for details. 
- Adding new tests for the existing code - Open an issue mentioning the specific section or function(s) of code you wish to add the test for. 

### Contribution workflow

- Open a new issue and describe your contribution.
- Get the source code.
- Set up a local development environment on your system.
- Work on your contribution, add your changes locally and submit a merge request according to the guidelines below. 


## Merge request guidelines

- Fork the miniff repository. This will create a copy of the miniff repostory on your GitLab account.
- Clone this fork of miniff on to your system.
- Step into the root directory of the cloned miniff on your system by executing `cd miniff`
- Create a new branch from the master branch to add your changes in. `git checkout -b <branch-name> master`
- Setup a local development environment as explained in the section [Set up a local miniff development environment](#Set-up-a-local-miniff-development-environment)
- Add your changes in this branch, build and test it locally to ensure that the changes are fine.
  - run `python setup.py build` and `python setup.py nosetests`
  - If you are making changes to the doucmentation, build and test the documentation locally as described in the section [Contributing to documentation](#Contributing-to-documentation).
- Commit the changes and push them to your fork of miniff.
- Create a merge request from the feature branch in your fork towards the master branch of the miniff repository. In the merge request description, additionaly reference the issue number by adding the text 'closes #<issuenumber>'. This will ensure that the referenced issue will automatically close upon the merge of this branch. 


## Set up a local miniff development environment

### Prerequisites

* Python3
* C compiler: Required for compiling Cython extensions

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

  On Windows, the support for installing a C compiler and compiling cython extensions is cumbersome and outdated as can be inferred from the [Cython Wiki](https://github.com/cython/cython/wiki/CythonExtensionsOnWindows).
  We recommend to use the Windows subsystem for Linux (WSL) in this case. More information on WSL and its installation instructions can be found [here](https://docs.microsoft.com/en-us/windows/wsl/install-win10).


### Installation steps

* Clone the repository on your system
   ```
   git clone https://gitlab.kwant-project.org/qt/miniff.git
   ```
   Move to the root of the project by executing `cd miniff/` and continue with the following steps from inside this directory.

* Install the dependencies via one of the two options below.

   * Option 1: If you have Conda installed already, use the provided [`environment.yml`](environment.yml) to create a miniff development environment.
     ```
     conda env create -n <my-env> -f environment.yml
     ```
     Activate the above created virtual environment 
     ```
     conda activate <my-env>
     ```

   * Option 2: Alternatively, you can use virtualenv to create a virtual environment, and install the dependencies via pip using the [`requirements.txt`](requirements.txt).
     ```
     $ virtualenv -p python3 .venv
     $ source .venv/bin/activate
     $ pip install -r requirements.txt
     ```

* Build and install `miniff` in editable mode.

   Use the provided [`setup.py`](setup.py).
   
   ```bash
   python3 setup.py build
   python3 setup.py develop
   ```

* Verify your installation by launching a python interpreter and executing `import miniff`, it should return no error.

   ```python
   python
   >>> import miniff
   >>>
   ```


## Contributing to documentation
Documentation for miniff is developed using Sphinx and is hosted on Read the Docs. The source of the documentation resides in the `docs/` directory and is written in RST (Restructured Text). The workflow for contributing to the documentation is the same as for contrbuting channges via new features or bugfixes. This workkflow is described in the section [Merge request guidelines](#Merge-request-guidelines)

The documentation can be built and tested locally in the following way.
- After you have added your changes, build the documentation by executing `make html` from inside the `docs/` diectory.
- A successfull build will create a `_build/` directory in `docs/`and populate it with the documentation rendered in html pages in the `html/` directory. You can open these html pages in your system's browser and verify your changes.
- If you installed any additional packages while adding changes to the documentation, please make sure to include them in `docs/requirements.txt` so that the dependencies are updated.
