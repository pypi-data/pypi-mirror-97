from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="sod",
    version="0.0.2",
    description="Load and write .sod files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GoodClover/sod",
    author="Oliver Simmons",
    author_email="oliversimmo@gmail.com",
    py_modules=["sod"],
    package_dir={"": "src"},
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
