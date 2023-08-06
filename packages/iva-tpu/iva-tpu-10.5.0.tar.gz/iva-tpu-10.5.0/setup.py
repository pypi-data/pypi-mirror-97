# coding: utf-8
"""Setup script for IVA TPU."""

from os import getenv
from setuptools import find_packages, setup
from distutils.extension import Extension
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='iva-tpu',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      version="10.5.0",
      author="Maxim Moroz",
      author_email="m.moroz@iva-tech.ru",
      description="IVA TPU Python API",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="http://git.mmp.iva-tech.ru/tpu_sw/pytpu",
      install_requires=[
            'numpy>=1.14',
            'Cython'
      ],
      zip_safe=False,
      ext_modules=cythonize([Extension("iva_tpu.tpu.tpu", ['src/iva_tpu/tpu/tpu.pyx'], libraries=["tpu"]), ],
                            compiler_directives={'language_level': "3"}
                            ),
      python_requires='>=3.6',
      )
