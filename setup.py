import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="truthtables",
    version="0.0.1",
    author="Ruben Purdy",
    author_email="rpurdy@andrew.cmu.edu",
    description="A library for working with truth tables in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rbnprdy/truthtables",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
