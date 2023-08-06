from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ambio",
    version="0.5.2",
    author="Alberto Mosconi",
    author_email="albertomaria.mosconi@gmail.com",
    description="A lightweight Bioinformatics library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/albertomosconi/ambio",
    project_urls={
        "Bug Tracker": "https://github.com/albertomosconi/ambio/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    extras_requires={
        "dev": [
            "pytest>=6.2.2",
        ],
    },
)
