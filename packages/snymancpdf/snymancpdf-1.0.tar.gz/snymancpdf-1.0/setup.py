import setuptools
from pathlib import Path

path_read_me = Path(
    "/Users/thegeneral/workspace/python/projects/cwm/snymancpdf/README.md")

setuptools.setup(
    name="snymancpdf",
    version=1.0,
    long_description=path_read_me.read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
