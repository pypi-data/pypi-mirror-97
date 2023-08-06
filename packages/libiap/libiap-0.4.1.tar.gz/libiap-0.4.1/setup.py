from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="libiap",
    version="0.4.1",
    packages=find_packages(),
    url="https://github.com/umccr-illumina/libiap",
    license="MIT",
    author="UMCCR and Contributors",
    author_email="services@umccr.org",
    description="Please use https://github.com/umccr-illumina/libica instead",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=[
        "libica==0.5.0",
    ],
    extras_require={
        "dev": [
            "twine",
            "setuptools",
            "wheel",
        ],
    },
    classifiers=[
        "Development Status :: 7 - Inactive",
    ],
)
