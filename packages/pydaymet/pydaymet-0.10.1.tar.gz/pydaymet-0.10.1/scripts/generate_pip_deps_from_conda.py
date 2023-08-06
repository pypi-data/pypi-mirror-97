#!/usr/bin/env python
"""Convert the conda environment.yml to the pip requirements-dev.txt.

It also checks that they have the same packages (for the CI).
The original script is taken from Pandas github repository.
https://github.com/pandas-dev/pandas/blob/master/scripts/generate_pip_deps_from_conda.py.

Usage
-----

    Generate `requirements-dev.txt`
    $ ./generate_pip_deps_from_conda.py

    Compare and fail (exit status != 0) if `requirements-dev.txt` has not been
    generated with this script:
    $ ./generate_pip_deps_from_conda.py --compare
"""
import argparse
import os
import re
import sys

import yaml

EXCLUDE = {"python", "pip"}
RENAME = {
    "pytables": "tables",
    "pyqt": "pyqt5",
    "dask-core": "dask",
    "matplotlib-base": "matplotlib",
    "seaborn-base": "seaborn",
    "git+https://github.com/cheginit/pygeoogc.git": "pygeoogc",
    "git+https://github.com/cheginit/pygeoutils.git": "pygeoutils",
    "git+https://github.com/cheginit/pynhd.git": "pynhd",
    "git+https://github.com/cheginit/py3dep.git": "py3dep",
    "git+https://github.com/cheginit/pydaymet.git": "pydaymet",
    "git+https://github.com/cheginit/pygeohydro.git": "pygeohydro",
}


def conda_package_to_pip(package):
    """Convert a conda package to its pip equivalent.

    In most cases they are the same, those are the exceptions:
    - Packages that should be excluded (in `EXCLUDE`)
    - Packages that should be renamed (in `RENAME`)
    - A package requiring a specific version, in conda is defined with a single
    equal (e.g. ``pandas=1.0``) and in pip with two (e.g. ``pandas==1.0``)
    """
    package = re.sub("(?<=[^<>])=", "==", package).strip()

    for compare in ("<=", ">=", "=="):
        if compare not in package:
            continue

        pkg, version = package.split(compare)
        if pkg in EXCLUDE:
            return

        if pkg in RENAME:
            return "".join((RENAME[pkg], compare, version))

        break

    if package in RENAME:
        return RENAME[package]

    return package


def main(conda_fname, pip_fname, compare=False):
    """Generate the pip dependencies file from the conda file.

    It also compares that they are synchronized (``compare=True``).

    Parameters
    ----------
    conda_fname : str
        Path to the conda file with dependencies (e.g. `environment.yml`).
    pip_fname : str
        Path to the pip file with dependencies (e.g. `requirements-dev.txt`).
    compare : bool, default False
        Whether to generate the pip file (``False``) or to compare if the
        pip file has been generated with this script and the last version
        of the conda file (``True``).

    Returns
    -------
    bool
        True if the comparison fails, False otherwise
    """
    with open(conda_fname) as conda_fd:
        deps = yaml.safe_load(conda_fd)["dependencies"]

    pip_deps = []
    for dep in deps:
        if isinstance(dep, str):
            conda_dep = conda_package_to_pip(dep)
            if conda_dep:
                pip_deps.append(conda_dep)
        elif isinstance(dep, dict) and len(dep) == 1 and "pip" in dep:  # noqa: SIM106
            pip_deps += dep["pip"]
        else:
            raise ValueError(f"Unexpected dependency {dep}")

    for i, dep in enumerate(pip_deps):
        if dep in RENAME:
            pip_deps[i] = RENAME[dep]

    if "pip" in pip_deps:
        pip_deps.remove("pip")

    fname = os.path.split(conda_fname)[1]
    header = (
        f"# This file is auto-generated from {fname}, do not modify.\n"
        "# See that file for comments about the need/usage of each dependency.\n\n"
    )
    pip_content = header + "\n".join(pip_deps)

    if compare:
        with open(pip_fname) as pip_fd:
            return pip_content != pip_fd.read()
    else:
        with open(pip_fname, "w") as pip_fd:
            pip_fd.write(pip_content)
        return False


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="convert (or compare) conda file to pip")
    argparser.add_argument(
        "--compare",
        action="store_true",
        help="compare whether the two files are equivalent",
    )
    args = argparser.parse_args()

    repo_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    res = main(
        os.path.join(repo_path, "ci/requirements/environment.yml"),
        os.path.join(repo_path, "requirements.txt"),
        compare=args.compare,
    )
    if res:
        msg = (
            f"`requirements-dev.txt` has to be generated with `{sys.argv[0]}` after "
            "`environment.yml` is modified.\n"
        )
        if args.azure:
            msg = f"##vso[task.logissue type=error;sourcepath=requirements-dev.txt]{msg}"
        sys.stderr.write(msg)
    sys.exit(res)
