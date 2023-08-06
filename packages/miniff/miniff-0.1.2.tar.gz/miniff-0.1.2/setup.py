#!/usr/bin/env python3
from setuptools import setup, find_packages
from setuptools.extension import Extension
from setuptools import Command
from Cython.Build import cythonize
from pathlib import Path
from string import Template, _ChainMap
import re
import json

import numpy

_sentinel_dict = {}


class IndentedTemplate(Template):

    def safe_substitute(self, mapping=_sentinel_dict, **kws):
        if mapping is _sentinel_dict:
            mapping = kws
        elif kws:
            mapping = _ChainMap(kws, mapping)
        # Helper function for .sub()
        def convert(mo):
            pattern = r"^(\s*)$"
            indent = re.findall(pattern, self.template[:mo.start()], re.MULTILINE)
            if len(indent) > 0:
                indent = indent[-1]
            else:
                indent = None

            # Check the most common path first.
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                try:
                    substitution = mapping[named]
                except KeyError:
                    return mo.group()
                if isinstance(substitution, (list, tuple)):
                    if indent is None:
                        raise ValueError(f"Cannot substitute multi-line '{named}'")
                    substitution = f"\n{indent}".join(substitution)
                return str(substitution)
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)
        return self.pattern.sub(convert, self.template)

    def substitute(self, mapping=_sentinel_dict, **kws):
        raise NotImplementedError


class BuildPotentials(Command):
    description = "build cython source for potentials"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run command."""
        # Read all templates
        templates = {}
        for i in Path("templates").glob("*.pyx"):
            with open(i, 'r') as f:
                templates[i.stem] = IndentedTemplate(f.read())

        # Construct serial and OpenMP templates
        serial = dict(
            range="range",
            range_args="",
            decorators="",
        )
        templates_serial = {k: IndentedTemplate(v.safe_substitute(**serial)) for k, v in templates.items()}

        parallel = dict(
            range="prange",
            range_args="nogil=True, schedule='static'",
            decorators="@cython.boundscheck(False)\n@cython.wraparound(False)",
        )
        templates_parallel = {k: IndentedTemplate(v.safe_substitute(**parallel)) for k, v in templates.items()}

        # Read all potentials
        with open("resources/potentials.json", 'r') as f:
            potentials = json.load(f)

        # Construct the contents of cython file
        parts = []
        defaults = dict(
            r12_symmetry_allowed="0",
            parameters='',
            degenerate=False,
            final_filter=True,
            openmp=True,
        )

        for k in "preamble", "preamble_grad", "before", "before_grad", "before1", "before1_grad", "before_inner", "before_inner_grad":
            defaults[k] = f"# (no '{k}' statements)"
        for p in potentials:
            _p = defaults.copy()
            _p.update(p)
            p = _p

            if len(p["parameters"]) > 0:
                p["parameters"] = ", ".join(i.strip() for i in p["parameters"].split(",")) + ","

            openmp = p.pop("openmp")
            template_kind = p.pop("type")
            name = p.pop("name")

            # Serial variant
            parts.append(templates_serial[template_kind].safe_substitute(name=f"kernel_{name}", **p))
            parts.append(templates_serial[f"{template_kind}-g"].safe_substitute(name=f"kernel_g_{name}", **p))

            if openmp:
                # Parallel variant
                parts.append(templates_parallel[template_kind].safe_substitute(name=f"pkernel_{name}", **p))
                parts.append(templates_parallel[f"{template_kind}-g"].safe_substitute(name=f"pkernel_g_{name}", **p))

        with open("miniff/_potentials.pyx", 'w') as f:
            f.write(templates["potentials"].safe_substitute(
                kernels="\n\n".join(parts),
            ))


class ext_modules_lazy(list):
    def __init__(self):
        self.ext_modules = None

    def eval(self):
        self.ext_modules = cythonize([
            Extension("miniff._potentials", ["miniff/_potentials.pyx"], include_dirs=[numpy.get_include()],
                      extra_compile_args=['-fopenmp'], extra_link_args=['-fopenmp']),
            Extension("miniff._util", ["miniff/_util.pyx"], include_dirs=[numpy.get_include()]),
        ], compiler_directives={"profile": True}, annotate=True)

    def __iter__(self):
        if self.ext_modules is None:
            self.eval()
        yield from self.ext_modules

    def __len__(self):
        if self.ext_modules is None:
            self.eval()
        return len(self.ext_modules)

    def __getitem__(self, item):
        if self.ext_modules is None:
            self.eval()
        return self.ext_modules[item]

setup(
    name='miniff',
    version='0.1.2',
    author='Artem Pulkin, Viacheslav Ostroukh '
           'Niket Agrawal, André Melo, Anastasiia Varentcova',
    author_email='gpulkin@gmail.com',
    packages=find_packages(),
    cmdclass={'potentials': BuildPotentials},
    test_suite="nose.collector",
    tests_require="nose",
    description='A minimal implementation of force fields',
    long_description=open('README.md').read(),
    ext_modules=ext_modules_lazy(),
    install_requires=[
        'numpy>=1.18',
        'scipy>=1.4',
        'numericalunits>=1.25',
        'matplotlib>=3.2',
        'torch>=1.5',
    ],
    scripts=[
    ],
)
