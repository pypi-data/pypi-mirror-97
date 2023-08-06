#!/usr/bin/env python
# Copyright (c) 2021, David Turner
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/davidt0x/py-spike-recorder for details.

from __future__ import print_function

import sys
import os

from setuptools import find_packages

try:
    from skbuild import setup
except ImportError:
    print(
        "Please update pip, you need pip 10 or greater,\n"
        " or you need to install the PEP 518 requirements in pyproject.toml yourself",
        file=sys.stderr,
    )
    raise

# We need to get the absolute path to the vcpkg toolchain file. It seems scikit-build
# invokes cmake two different times (one for a cmake_test_compile). Each of these times
# the directory it invokes from is different so a relative path won't work. ../../
# works for the test compile but we need ../../../ for the skbuild one. Absolute path
# gets around this. Though, I think the code below will break if there are spaces in the
# path on the machine. Whenever I tried to quote the path it would not work.
vcpkg_toolchain_path = os.path.abspath('extern/Spike-Recorder/vcpkg/scripts/buildsystems/vcpkg.cmake')

# Setup the arguments for cmake, enable vcpkg by passing the tool chain file
cmake_args = ['-GNinja',  f'-DCMAKE_TOOLCHAIN_FILE={vcpkg_toolchain_path}']

# If this is windows, make sure we build everything statically, that we can at least.
if sys.platform.startswith('win'):
    cmake_args.append('-DVCPKG_TARGET_TRIPLET=x64-windows-static')

setup(
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    zip_safe=False,
    include_package_data=True,
    cmake_install_dir="src/spike_recorder/server",
    cmake_args=cmake_args
)
