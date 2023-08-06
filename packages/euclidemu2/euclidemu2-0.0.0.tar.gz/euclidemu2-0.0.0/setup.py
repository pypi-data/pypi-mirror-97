from setuptools import setup, Extension, find_packages
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import os
from distutils.sysconfig import get_python_lib

os.environ["CC"] = "g++"
os.environ["CXX"] = "g++"

if 'LDFLAGS' in os.environ.keys():
    ldfl=os.environ['LDFLAGS']
    new_ldfl=ldfl.replace('-Wl,-dead_strip_dylibs ','')
    os.environ['LDFLAGS']=new_ldfl


pathtopythonlib=get_python_lib()

with open("README.md", 'r') as f:
    long_description = f.read()

pack_name='euclidemu2'

extensions=Extension(name=pack_name,
                           sources=["src/euclidemu2.pyx","src/cosmo.cxx","src/emulator.cxx"],
                           include_dirs=["/usr/local/include","../src/"],
                           libraries=["gsl","gslcblas"],
                           extra_link_args=['-L/usr/local/lib'],
                           language="c++",
                           extra_compile_args=['-std=c++11',
                                               '-D PATH_TO_EE2_DATA_FILE="'+pathtopythonlib+'/'+pack_name+'/ee2_bindata.dat"']
                           )


setup(name=pack_name,
      version="0.0.0",
      author="Pedro Carrilho,  Mischa Knabenhans",
      description="Python wrapper for EuclidEmulator2",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://github.com/PedroCarrilho/EuclidEmulator2/tree/pywrapper",
      cmdclass={'build_ext': build_ext},
      ext_modules = cythonize(extensions,language_level = 3),
      packages=[pack_name],
      package_dir={pack_name: 'src'},
      package_data={pack_name: ["ee2_bindata.dat","cosmo.h","emulator.h","units_and_constants.h"]},
      include_package_data=True,
      install_requires=['cython','numpy','scipy']
      )
