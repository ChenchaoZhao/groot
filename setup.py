from setuptools import find_packages, setup

from groot import __version__

# load readme
with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="groot",
    version=__version__,
    author="Chenchao Zhao",
    author_email="chenchao.zhao@gmail.com",
    description="Manage hierarchical concept trees with style.",
    packages=find_packages(exclude=["tests"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["dataclasses"],
    license="MIT",
)
