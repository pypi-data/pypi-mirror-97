#!/usr/bin/env python

#    Copyright 2021 SolarWinds, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import io
import os
import re
import sys
from distutils import log
from distutils.command.build import build

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

version = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', io.open('appoptics_apm/version.py', encoding='utf_8').read()).group(1)


def is_alpine_distro():
    # checking alpine dist
    if os.path.exists("/etc/alpine-release"):
        return True

    try:
        with open("/etc/os-release", 'r') as osr:
            releases = osr.readlines()
            releases = [l[:-1] for l in releases]
        if 'NAME="Alpine Linux"' in releases:
            return True
    except Exception:
        pass

    return False


def python_version_supported():
    if sys.version_info[0] == 2:
        if sys.version_info[1] not in (7, ):
            return False
    elif sys.version_info[0] == 3:
        if sys.version_info[1] < 4:
            return False
    return True


def choose_oboe():
    log.info("[SETUP] choose to link to platform specific liboboe")
    root = './appoptics_apm/swig'
    liboboe = "liboboe-1.0-x86_64.so.0.0.0"
    alpineoboe = "liboboe-1.0-alpine-x86_64.so.0.0.0"
    tmp_oboe = "/".join([root, liboboe])
    tmp_alpine = "/".join([root, alpineoboe])

    # choose platform compatible oboe and rename it to default name
    try:
        if is_alpine_distro():
            if os.path.exists(tmp_oboe):
                os.remove(tmp_oboe)
            if os.path.exists(tmp_alpine):
                os.renames(tmp_alpine, tmp_oboe)
        else:
            # assume all others are g-libc compatible
            if os.path.exists(tmp_alpine):
                os.remove(tmp_alpine)

        # liboboe should have been removed for darwin, create symlink for others
        if os.path.exists(tmp_oboe):
            for lib in ['liboboe-1.0.so', 'liboboe-1.0.so.0']:
                lib_path = "/".join([root, lib])
                if os.path.exists(lib_path):
                    os.remove(lib_path)
                    log.info("remove liboboe links %s" % lib_path)
                os.symlink(liboboe, lib_path)

    except Exception as ecp:
        log.info("[SETUP] failed to set up platform specific oboe... {e}".format(e=ecp))


def os_supported():
    return sys.platform.startswith('linux')


if not (python_version_supported() and os_supported()):
    log.warn(
        "[SETUP] This package supports only Python 2.7, 3.4 and above on Linux"
        "Other platform or python versions may not work as expected.")

ext_modules = [
    Extension(
        'appoptics_apm.swig._oboe',
        sources=['appoptics_apm/swig/oboe_wrap.cxx', 'appoptics_apm/swig/oboe_api.cpp'],
        depends=['appoptics_apm/swig/oboe_api.hpp'],
        include_dirs=['appoptics_apm/swig', 'appoptics_apm'],
        libraries=['oboe-1.0', 'rt'],
        library_dirs=['appoptics_apm/swig'],
        extra_compile_args=["-std=c++11"],
        runtime_library_dirs=['$ORIGIN']),
]


class CustomBuild(build):
    def run(self):
        self.run_command('build_ext')
        build.run(self)


class CustomBuildExt(build_ext):
    def run(self):
        if sys.platform == 'darwin':
            return
        choose_oboe()
        build_ext.run(self)


with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='appoptics_apm',
    cmdclass={
        'build_ext': CustomBuildExt,
        'build': CustomBuild,
    },
    version=version,
    author='SolarWinds, LLC',
    author_email='support@appoptics.com',
    url='https://www.appoptics.com/monitor/python-performance',
    download_url='https://pypi.python.org/pypi/appoptics_apm',
    description='AppOptics APM libraries, instrumentation, and web middleware components '
    'for WSGI, Django, and Tornado.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='appoptics_apm traceview tracelytics oboe liboboe instrumentation performance wsgi middleware django',
    ext_modules=ext_modules,
    packages=['appoptics_apm', 'appoptics_apm.swig'],
    package_data={
        'appoptics_apm': ['swig/liboboe-1.0.so.0', 'swig/VERSION', 'swig/bson/bson.h', 'swig/bson/platform_hacks.h']
    },
    license='LICENSE',
    install_requires=['decorator', 'six'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
