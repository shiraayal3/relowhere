from setuptools import find_packages, setup

setup(
    name="relowhere",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
)
