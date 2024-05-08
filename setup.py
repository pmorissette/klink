import codecs
import os
from setuptools import setup

from klink import __version__


def local_file(filename):
    return codecs.open(os.path.join(os.path.dirname(__file__), filename), "r", "utf-8")


setup(
    name="klink",
    version=__version__,
    author="Philippe Morissette",
    author_email="morissette.philippe@gmail.com",
    description="Klink is a simple and clean theme for creating Sphinx docs, inspired by jrnl",
    long_description=local_file("README.rst").read().replace("\r\n", "\n"),
    url="https://github.com/pmorissette/klink",
    license="MIT",
    install_requires=[
        "sphinx",
    ],
    extras_require={
        "dev": [
            "isort>=5,<6",
            "ruff>=0.3,<0.4",
            "twine",
            "wheel",
        ],
    },
    packages=["klink"],
    package_data={
        "klink": [
            "theme.conf",
            "layout.html",
            "static/css/klink.css",
            "static/fonts/*.*",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
    ],
    python_requires=">=3.7",
)
