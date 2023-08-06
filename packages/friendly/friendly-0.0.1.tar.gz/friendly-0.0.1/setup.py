# pylint: skip-file
from setuptools import setup
from friendly import __version__

with open("README.md", encoding="utf8") as f:
    README = f.read()

setup(
    name="friendly",
    version=__version__,
    description="Major project to be imported here - soon",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    url="https://github.com/aroberge/ftemp",
    author="André Roberge",
    author_email="Andre.Roberge@gmail.com",
    py_modules=["friendly"],
    python_requires=">=3.6",
)
