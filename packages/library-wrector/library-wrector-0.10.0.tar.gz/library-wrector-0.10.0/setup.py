import os
from typing import List

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Use VERSION as the source of truth
# copy it to marian_library/version.py
# for use in module.__version__ property
with open(os.path.join(here, "VERSION"), encoding="utf-8") as f:
    __version__ = f.read().strip()
    with open(
        os.path.join(here, "library_wrector", "version.py"), "w+", encoding="utf-8"
    ) as v:
        v.write("# CHANGES HERE HAVE NO EFFECT: ../VERSION is the source of truth\n")
        v.write(f'__version__ = "{__version__}"')

install_requires = [
                        "torch==1.5.0",
                        "allennlp==0.8.4",
                        "python-Levenshtein==0.12.0",
                        "transformers==2.2.2",
                        "scikit-learn==0.20.0",
                        "sentencepiece==0.1.91"
]

setup(
    name="library-wrector",
    description="",
    packages=find_packages(),
    package_data={"library_wrector": ["data/*"]},
    include_package_data=True,
    author="Writer",
    author_email="melisa@qordoba.com",
    url="https://github.com/Qordobacode/library.wrector",
    version=__version__,
    license="unlicensed",
    long_description="",#long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Typing :: Typed",
    ],
)