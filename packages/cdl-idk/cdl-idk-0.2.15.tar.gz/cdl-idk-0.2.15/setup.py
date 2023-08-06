"""
Tools for building insight generators.
"""

from idk._version import __version__

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import find_packages, setup

with open("README.md") as fp:
    long_description = fp.read()


setup(
    name="cdl-idk",
    version=__version__,
    description="Tools for building insight generators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="eden.trainor@compassdigital.io",
    packages=["idk"],
    install_requires=[
        "requests",
        "mypy",
        "pandas"
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": ["idk=idk._cli:main"]
    },
    package_data={
        "idk": ["templates/*.py"]
    }
)
