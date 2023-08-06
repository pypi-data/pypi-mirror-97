from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fathom-lib", 
    version="0.1.2",
    description="Fathom lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fathoms-io/fathom-lib",
    project_urls={
        "Bug Tracker": "https://github.com/fathoms-io/fathom-lib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
)