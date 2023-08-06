#!/usr/bin/env python3

# https://packaging.python.org/tutorials/packaging-projects/
# https://packaging.python.org/guides/distributing-packages-using-setuptools/

import setuptools

import Agunua

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="agunua", 
    version=Agunua.VERSION,
    author="Stéphane Bortzmeyer",
    author_email="stephane+framagit@bortzmeyer.org",
    description="A library for the development of Gemini clients",
    keywords="Gemini",
    license="GPL",
    install_requires=['pyopenssl'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://framagit.org/bortzmeyer/agunua/",
    packages=["Agunua"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    package_data={
        "Agunua": ["sample-client.py", "README.md", "LICENSE", "CHANGES"]
    },
    scripts=["agunua"]
)
