from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sweetspot-sdk",
    version="0.0.5",
    description="SDK for Sweetspot Team to interact with backend APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Philip Kung",
    author_email="philip@sweetspot.so",
    url="https://www.sweetspot.so",
    packages=find_packages(),
    install_requires=[
        'requests>=2.9.1, <3.0',
        'jsonpickle>=1.4, >= 1.4.1',
        'python-dateutil>=2.5.3, <3.0',
        'deprecation>=2.0.6'
    ]
)