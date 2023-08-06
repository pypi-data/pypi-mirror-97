import os
import re
import sys
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable,
                      '-DUSE_PYTHON=1']

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)


MIN_PYBIND_VER = '2.5.0'

def read_version_from_header():
    with open('include/gemmi/version.hpp') as f:
        for line in f:
            if line.startswith('#define GEMMI_VERSION '):
                return line.split()[2].strip('"dev')

__version__ = read_version_from_header()

setup(
    name='gemmi',
    version=__version__,
    author='Marcin Wojdyr',
    author_email='wojdyr@gmail.com',
    url='https://project-gemmi.github.io/',
    description='library for structural biology',
    long_description='''\
    Library for macromolecular crystallography and structural bioinformatics.
    For working with coordinate files (mmCIF, PDB, mmJSON),
    refinement restraints (monomer library), electron density maps (CCP4),
    and crystallographic reflection data (MTZ, SF-mmCIF). It understands
    crystallographic symmetries, it knows how to switch between the real
    and reciprocal space and it can do a few other things.

    The setup.py script builds only Python extension.
    Use cmake to build also a command-line program.
    ''',
    ext_modules=[CMakeExtension('gemmi')],
    packages=['gemmi-examples'],
    package_dir={'gemmi-examples': 'examples'},
    install_requires=['pybind11>=' + MIN_PYBIND_VER],
    setup_requires=['pybind11>=' + MIN_PYBIND_VER],
    cmdclass={'build_ext': CMakeBuild},
    zip_safe=False,
    license='MPL-2.0',
    keywords=('structural bioinformatics, structural biology, crystallography,'
              ' CIF, mmCIF, PDB, CCP4, MTZ'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Programming Language :: C++',
        'Programming Language :: Python',
    ],
)
