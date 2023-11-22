# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext, ParallelCompile
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.build import _build
import subprocess

import os.path as path

from glob import glob

__version__ = "4.2.1"


dunedaq_packages = [
    'detdataformats',
    'fddetdataformats',
    'daqdataformats',
    'trgdataformats',
    # 'detchannelmaps',
    'rawdatautils'
]

packages = dunedaq_packages[:]

package_dir = { p:f"dunedaq/{p}/python/{p}" for p in dunedaq_packages }

# package_dir = {
#     'detdataformats': 'dunedaq/detdataformats/python/detdataformats',
#     'fddetdataformats': 'dunedaq/fddetdataformats/python/fddetdataformats'
# }


# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

# ext_modules = [
#     Pybind11Extension(
#         "detdataformats/_daq_detdataformats_py",
#         sources=[
#             # "src/main.cpp",
#         ] + glob('dunedaq/detdataformats/pybindsrc/*.cpp'),
#         include_dirs=[
#             "dunedaq/detdataformats/include"
#         ],
#         # Example: passing in the version to the compiled code
#         define_macros=[("VERSION_INFO", __version__)],
#     ),
#     Pybind11Extension(
#         "fddetdataformats/_daq_fddetdataformats_py",
#         sources=[
#             # "src/main.cpp",
#         ] + glob('dunedaq/fddetdataformats/pybindsrc/*.cpp'),
#         include_dirs=[
#             "dunedaq/detdataformats/include",
#             "dunedaq/fddetdataformats/include"
#         ],
#         # Example: passing in the version to the compiled code
#         define_macros=[("VERSION_INFO", __version__)],
#     ),
# ]


class build(_build):
    def run(self):
        dir_path = path.dirname(path.realpath(__file__))
        sm_init_res = subprocess.check_output(['git', 'submodule', 'update', '--init', '--recursive'], cwd=dir_path)
        print(sm_init_res)


        # ---- some custom code here ----
        # important to do this instead of "super", since it hasn't been properly updated
        _build.run(self) 

ext_modules = [
    Pybind11Extension(
        f"{p}/_daq_{p}_py",
        sources=[
            # "src/main.cpp",
        ] + glob(f"dunedaq/{p}/pybindsrc/*.cpp"),
        include_dirs=[
            # Brute force
            f"dunedaq/{i}/include" for i in dunedaq_packages 
        ],
        # Example: passing in the version to the compiled code
        define_macros=[("VERSION_INFO", __version__)],
    ) for p in dunedaq_packages
]

with ParallelCompile("NPY_NUM_BUILD_JOBS"):
    setup(
        name="datafmt",
        version=__version__,
        author="Alessandro Thea",
        author_email="alessandro.thea@gmail.com",
        url="https://github.com/alessandrothea/datafmt",
        description="A test project using pybind11",
        long_description="",
        packages=packages,
        package_dir=package_dir,
        ext_modules=ext_modules,
        extras_require={"test": "pytest"},
        # Currently, build_ext only provides an optional "highest supported C++
        # level" feature, but in the future it may provide more features.
        cmdclass={
            "build": build,
            "build_ext": build_ext,
            },
        zip_safe=False,
        python_requires=">=3.7",
    )
