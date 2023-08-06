import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cbmi_utils",
    version="0.1.13",
    author="Patrick Baumann",
    author_email="Patrick.Baumann@htw-berlin.de",
    description="Utility package for common features at CBMI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.tools.f4.htw-berlin.de/baumapa/cbmi_utils",
    packages=setuptools.find_packages(
        exclude=(
            "tests",
        )
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "torch>=1.7.1",
        "torchvision>=0.8.2",
    ],
)
