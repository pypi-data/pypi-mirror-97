from setuptools import setup, find_packages
from version import __version__

name = "modelindex"
author = "Robert Stojnic"
author_email = "hello@paperswithcode.com"
url = "https://github.com/paperswithcode/modelindex-alias"


setup(
    name=name,
    version=__version__,
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    description="This is an alias for the model-index library.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url=url,
    platforms=["Windows", "POSIX", "MacOSX"],
    license="MIT",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
)
