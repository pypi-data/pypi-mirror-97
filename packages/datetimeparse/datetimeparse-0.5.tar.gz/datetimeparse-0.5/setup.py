import setuptools
import distutils
from Cython.Build import cythonize


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION.txt", "r") as fh:
    version = fh.read().strip()


setuptools.setup(
    name='datetimeparse',
    version=0.5,
    author="Kevin Crouse",
    author_email="krcrouse@gmail.com",
    description="A fast utility to parse and output timestamps in ISO8601/RFC3339 format, written mostly in C.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/krcrouse/datetimeparse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    ext_modules=cythonize([
        setuptools.Extension(
            "datetimeparse",
            sources=[
                "cythonlib/datetimeparse.pyx", 
                "clib/datetimeparselib.c",
            ],
            include_dirs=["clib"], # location of .h
            #library_dirs=["clib"], # location of .c
        ),
        ],
        compiler_directives={
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
            'language_level': 3,
            'c_string_encoding': 'default',
            'iterable_coroutine': False,
        },
    )
 )


