from setuptools import setup
from klink import __version__

setup(
    name='klink',
    version=__version__,
    author='Philippe Morissette',
    author_email='morissette.philippe@gmail.com',
    description='Klink is a simple and clean theme for creating Sphinx docs, inspired by jrnl',
    url='https://github.com/pmorissette/klink',
    license='MIT',
    install_requires=[
        "sphinx",
    ],
    extras_require={
        "dev": [
            "black>=20.8b1",
            "flake8",
            "flake8-black",
        ],
    },
    packages=['klink'],
    package_data = {'klink': [
        'theme.conf',
        'layout.html',
        'static/css/klink.css',
        'static/fonts/*.*',
    ]},
)
