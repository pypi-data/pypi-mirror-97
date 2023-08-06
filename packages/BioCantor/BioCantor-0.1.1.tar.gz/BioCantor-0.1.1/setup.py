import itertools
import re
from pathlib import Path

from setuptools import find_namespace_packages, setup


def get_version() -> str:
    """Return package version as listed in `__version__` in `init.py`.

    Adapted from ``setup.py`` from https://github.com/encode/httpx.

    """
    version = Path("inscripta", "biocantor", "__init__.py").read_text()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", version).group(1)


dependencies = []

extra_dependencies = {
    "libraries": ["biopython"],
    "test": ["black", "flake8", "pytest", "pytest-cov", "pytest-flake8"],
    "docs": [
        "Sphinx",
        "sphinx_rtd_theme",
        "sphinx-automodapi",
        "graphviz",
        "nbconvert",
        "nbsphinx",
        "ipykernel",
        "pandoc",
    ],
    "optional": ["tornado>=5.1"],
}

all_dependencies = list(itertools.chain.from_iterable(extra_dependencies.values()))
extra_dependencies["all"] = all_dependencies

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="BioCantor",
    version=get_version(),
    description="Flexible feature arithmetic, seamlessly integrated with nested coordinate systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Inscripta, Inc.",
    url="https://github.com/InscriptaLabs/BioCantor",
    test_suite="pytest",
    packages=find_namespace_packages(include=["inscripta.*"]),
    include_package_data=True,
    tests_require=extra_dependencies["test"],
    extras_require=extra_dependencies,
    install_requires=dependencies,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
