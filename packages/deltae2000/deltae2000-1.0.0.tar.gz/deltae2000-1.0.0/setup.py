import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    README = f.read()


setup(
    name="deltae2000",
    version="1.0.0",
    description="deltae2000 implements an algorithm for perceptual distance between colours in pure Python.",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: MIT License",
    ],
    author="Landreville",
    url="https://gitlab.com/landreville/deltae2000",
    packages=find_packages(),
    install_requires=["colormath"],
)
