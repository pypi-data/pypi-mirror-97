# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aim_build']

package_data = \
{'': ['*']}

install_requires = \
['cerberus>=1.3,<2.0',
 'ninja-syntax>=1.7,<2.0',
 'tabulate>=0.8.7,<0.9.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['aim = aim_build.main:entry']}

setup_kwargs = {
    'name': 'aim-build',
    'version': '0.1.27',
    'description': 'A powerful and easy to use build tool for C++.',
    'long_description': '<p align="center">\n<img src="https://github.com/diwalkerdev/Assets/blob/master/Aim/aim.png" width="300" height="300">\n</p>\n\n![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/diwalkerdev/aim?include_prereleases)\n![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/diwalkerdev/aim/latest/dev?include_prereleases)\n![Python package](https://github.com/diwalkerdev/Aim/workflows/Python%20package/badge.svg?branch=dev)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aim-build)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/aim-build)\n![GitHub contributors](https://img.shields.io/github/contributors/diwalkerdev/aim)\n![GitHub](https://img.shields.io/github/license/diwalkerdev/aim)\n\n# Aim\nA command line tool for building C++ projects. \n\n## Introduction\nAim is an attempt to make building C++ projects from source as simple as possible while encouraging a modular approach \nto software development.\n\nAim only requires a `target.toml` file which is used to specify the builds of your project. Each build specifies a\ncomponent of your project, like a static library, dynamic library, or an executable.\n\n\n## Getting Started\n### Prerequisites\nAim requires the following dependencies:\n* [python](https://www.python.org/) - version 3.7 or above.\n* [ninja](https://ninja-build.org/)\n* [poetry](https://python-poetry.org/) - for development only\n\n### Installation\nAim is a `python` project and is installed using `pip`.\n\n```\npip install --user aim-build\n```\n\n### Using\n\nThere are 3 main commands:\n* `init` - initialises a directory with an empty project structure\n* `list --target=path/to/target_toml_dir` - displays the builds for the target\n* `build --target=path/to/target_toml_dir <build name>` - executes a build\n\nFor more information run:\n```\naim <command> --help\n```\n\nThe easiest way to get started is to use `aim init --demo-files`. `aim init` can be used to generate an empty\nproject structure and the `--demo-files` flags will copy a small test application into the current directory for \ndemonstration purposes.\n\nYou can then list the available builds of a target by specifying:\n\n`aim list --target=builds/linux-clang++-debug`\n\nAnd to build:\n\n`aim build --target=builds/linux-clang++-debug <build name>`\n\n<img src="https://github.com/diwalkerdev/Assets/blob/master/Aim/aim-init-demo.gif?raw=true" width="600px">\n\n## Target files\nA `target.toml` file describes a project and its build components.\n\nBegin by specifying the project root which is the path from the target file to your source files. All relative paths \nwill be relative to this directory.\n\nThe compiler frontend informs Aim how to construct compiler arguments. Next specify the compiler, archiver, flags and\nany defines. \n```\nprojectRoot = "../.."\n\ncompilerFrontend="gcc"\ncompiler = "clang++"\nar = "ar"\n\nflags = [\n    "-std=c++17",\n    "-O3",\n    "-g",\n    "-Wall",\n]\n\n# defines = [...]\n```\n\nNext specify your builds. For each build you must specify the `name` and `buildRule`. Valid build rules are `staticLib`,\n`dynamicLib`, `exe`, `headerOnly` or `libraryReference`. A build typically looks like:\n\n```\n[[builds]]\n    name = "calculatorApp"\n    buildRule = "exe"\n    requires = ["calculatorDynamic"] # A list of dependancies for this build.\n    outputName = "CalculatorApp"     # The output name. Aim will manage any prefixes or suffixes required.\n    srcDirs = ["src"]                # A list of source directories.\n    includePaths = ["include"]       # A list of include paths.\n    # The libraryPaths and libraries fields can be used to specify additional\n    # libraries and paths to the build. This allows for linking against third\n    # party libraries.\n    #libraryPaths = []\n    #libraries = []\n```\n\nAim will automatically generate the correct flags to use dependencies specified in the `requires` field.\n\nA `headerOnly` build does not have an `outputName` or `srcDirs`. It exists only so the `includePaths` can be imported\ninto another build using the `requires` field.\n\nA `libraryReference` does not have `srcDirs`. It exists only so the `includePaths`, `libraries` and `libraryPaths` field\ncan be imported into another build using the `requires` field.\n\nThe fields `compiler`, `flags` and `defines` are normally written at the top of the target file before the builds \nsection. By default, all builds will use these fields i.e. they are global, but they can also be overridden by specifying \nthem again in a build. Note that when these fields are specified specifically for a build, they completely replace the global\ndefinition; any `flags` or `defines` that you specify must be written out in full as they will not share\nany values with the global definition.\n\n## Methodology\nAim treats any build variation as its own unique build target with its own unique `target.toml`. \n\nA build target is some combination of _things_ that affects the output binary such as:\n * operating system (Windows, OSX, Gnu Linux)\n * compiler (MSVC, GCC, Clang)\n * build type (Release, Debug, Sanitized)\n * etc. \n \nEach build target and corresponding `target.toml` file must have its own directory ideally named using a unique \nidentifier that comprises the \'parts\' that make up the build. For example, the target file in the directory \n`linux-clang++-release` indicates that the toml file describes a project that is a `release` build, uses the `clang++`\ncompiler and is for the `linux` operating system. \n\nNote: each `target.toml` file must be written out in full for each target that you need to support. There is no way for\ntarget files to share information or to depend on another. While this leads to duplication between target files, it \nmakes them very explicit and makes debugging builds much easier.\n\n## Developing Aim\n\nAim is a Python project and uses the [poetry](https://python-poetry.org/) dependency manager. See [poetry installation](https://python-poetry.org/docs/#installation) for instructions.\n\nOnce you have cloned the project, the virtual environment and dependencies can be installed simply by executing:\n\n```\npoetry install\n```\n\n### Dev Install\nUnfortunately, unlike `setuptools`, there is no means to do a \'dev install\' using poetry. A dev install uses the\nactive source files under development, so the application can be tested without being installed each time.\n\nIn order to use Aim on the command line, is it recommended creating an alias. The alias needs to:\n* adds Aim to `PYTHONPATH` to resolve import/module paths \n* execute the main Aim script using virtualenv\'s python\n\nAim provides a `dev-env.bash` and `dev-env.fish` for setting an alias to mimic a \'dev\' install. These files must be\nsourced.\n\n   \n## Known Limitations\n* Windows support is still in development but is coming soon.\n',
    'author': 'David Walker',
    'author_email': 'diwalkerdev@twitter.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/diwalkerdev/Aim',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
