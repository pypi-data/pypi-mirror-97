from __VERSION__ import VERSION
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name="pyobe",
    version=VERSION,
    author="Jannchie",
    author_email="jannchie@gmail.com",
    description="Probe system for crawl data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jannchie/pyobe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['aiohttp'],
    python_requires='>=3.8',
)
