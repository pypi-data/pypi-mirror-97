import setuptools
from pathlib import Path

setuptools.setup(
    name="sgdot",
    version=1.27,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(
        exclude=["tests", "sgdot/data", "sgdot/examples"]),
    install_requires=Path("requirements.txt").read_text().split("\n")[:-1]
)
