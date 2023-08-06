"""Setup module for Rubin Jupyter Config object.
"""
import codecs
import io
import os
import setuptools


def get_version(file, name="__version__"):
    """Get the version of the package from the given file by
    executing it and extracting the given `name`.
    """
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]


def local_read(filename):
    """Convenience function for includes."""
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), filename
    )
    return codecs.open(full_filename, "r", "utf-8").read()


NAME = "rubin_jupyter_utils.config"
_path = NAME.replace(".", "/")
DESCRIPTION = "Rubin Jupyter Config object"
LONG_DESCRIPTION = local_read("README.md")
VERSION = get_version("%s/_version.py" % _path)
AUTHOR = "Adam Thornton"
AUTHOR_EMAIL = "athornton@lsst.org"
URL = "https://github.com/lsst-sqre/rubin-jupyter-config"
LICENSE = "MIT"

setuptools.setup(
    name=NAME,
    version=VERSION,
    long_description=LONG_DESCRIPTION,
    packages=setuptools.find_namespace_packages(
        include=["rubin_jupyter_utils.*"]
    ),
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
    keywords=["rubin", "jupyter", "config"],
    install_requires=[
        "eliot>=1,<2",
        "eliot-tree>=19,<20",
        "jupyter-client>=6,<7",
        "rubin_jupyter_utils.helpers>=0.31.0,<1.0",
    ],
)
