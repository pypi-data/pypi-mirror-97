import setuptools
from numpy.distutils.core import Extension, setup
from numpy.distutils.fcompiler import get_default_fcompiler

# setup fortran 90 extension
# ---------------------------------------------------------------------------

compiler = get_default_fcompiler()
 # set some fortran compiler-dependent flags
f90flags = []
if compiler == 'gnu95':
    f90flags.append('-ffree-line-length-none')
elif compiler == 'intel' or compiler == 'intelem':
    pass
f90flags.append('-O3')

ext1 = Extension(
    name="pyoculus_spec_fortran_module",
    sources=[
        "pyoculus/problems/SPECfortran/pyvariables.f90",
        "pyoculus/problems/SPECfortran/pybasefn.f90",
        "pyoculus/problems/SPECfortran/pycoords.f90",
        "pyoculus/problems/SPECfortran/pybfield.f90",
        "pyoculus/problems/SPECfortran/pyPJH.f90"
    ],
    extra_f90_compile_args=f90flags
)

install_requires = [
    "numpy",
    "scipy",
    "importlib-metadata ; python_version<'3.8'"
]
    

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyoculus",
    version='0.1.3',
    description="A Python version of Oculus - The eye into the chaos: a comprehensive magnetic field diagnostic package for non-integrable, toroidal magnetic fields",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License ",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
    url="https://github.com/zhisong/pyoculus",
    author="Zhisong Qu, Arunav Kumar, Stuart Hudson",
    license="MIT",
    packages=setuptools.find_packages(),
    package_data={"": ["pyoculus/problems/SPECfortran/*.f90"]},
    include_package_data=True,
    install_requires=install_requires,
    ext_modules=[ext1],
    setup_requires=["wheel"],
)
