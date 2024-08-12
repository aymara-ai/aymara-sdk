"""Aymara AI Python SDK."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = fh.read().splitlines()

setup(
    name="aymara-ai",
    version="0.1.0",
    author="Aymara AI",
    author_email="contact@aymara.ai",
    description="A Python SDK for using Ayamra to test your AI alignment.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.7",
    install_requires=install_requires,
)
