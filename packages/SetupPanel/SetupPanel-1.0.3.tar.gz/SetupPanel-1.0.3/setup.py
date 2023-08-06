import os
from setuptools import setup

_VERSION = "1.0.3"


with open(os.path.abspath("./README.md"), "r") as file:
    readme = file.read()


setup(
    name="SetupPanel",
    version=_VERSION,
    description="Intuitive and flexible configuration of interactive embed-based setup panels for discord.py",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/marwynnsomridhivej/setuppanel",
    author="Marwynn Somridhivej",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["setuppanel"],
    include_package_data=True,
    extras_require = {
        "dpy": ["discord.py"],
        "dpyv": ["discord.py[voice]"],
    }
)