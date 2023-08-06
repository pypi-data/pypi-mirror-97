import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="viant-cloudutils",
    version="0.1.3",
    author="Lee Sautia",
    author_email="lsautia@viantinc.com",
    description="Cloud utilities for automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.vianttech.com/techops/cloudutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
