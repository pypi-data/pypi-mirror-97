import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="histodata",
    version="0.2.7",
    author="Jonas Annuscheit",
    author_email="Jonas.Annuscheit@htw-berlin.de",
    description="Histopathology datasets for PyTorch environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.tools.f4.htw-berlin.de/cbmi-charite/histodata",
    packages=setuptools.find_packages(
        exclude=(
            "examples",
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
        "imagesize==1.2.0",
        "tiatoolbox==0.5.1",
        "torchvision>=0.6.1",
    ],
)
