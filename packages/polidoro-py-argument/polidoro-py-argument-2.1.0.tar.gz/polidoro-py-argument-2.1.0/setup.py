"""
Setup to create the package
"""
import setuptools

import polidoro_argument

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='polidoro-py-argument',
    version=polidoro_argument.VERSION,
    description='Package to create command line arguments for Python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/heitorpolidoro/py-argument',
    author='Heitor Polidoro',
    # author_email='heitor.polidoro',
    license='unlicense',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)
