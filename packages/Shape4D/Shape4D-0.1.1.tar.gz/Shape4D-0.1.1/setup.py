import setuptools
requires = ['numpy>=1.19.3']
from codecs import open
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Shape4D", # one's own name
    version="0.1.1",
    author="Liqun He, WanZheng He, Jun Hu",
    author_email="heliqun@ustc.edu.cn",
    description="A small library for visible 3D shapes",
    long_description="README.md",
    long_description_content_type="text/markdown",
    url="",
    include_package_data = True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)