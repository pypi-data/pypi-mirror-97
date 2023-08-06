import setuptools
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="polymatrix",
    version="0.0.4",
    description="Tools for simulating and solving polymatrix games.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Oskar Person",
    author_email="",
    license="MIT License",
    packages=setuptools.find_packages(exclude=['tests']),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "scipy>=1.4.0",
        "tqdm>=4.41.0",
        "networkx>=2.5.0",
        "numpy>=1.19.0"
    ],
    url="https://github.com/python-polymatrix-games/polymatrix",
    zip_safe=False,
)