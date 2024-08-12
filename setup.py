from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aymara-ai",
    version="0.1.0",
    author="Aymara AI",
    author_email="contact@aymara.ai",
    description="A Python SDK for using Ayamra to test your AI alignment.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "examples"]),
    python_requires=">=3.7",
    install_requires=[
        "pydantic>=2.6.1",
        "requests>=2.28.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=20.8b1",
            "isort>=5.7.0",
            "mypy>=0.800",
            "python-dotenv>=1.0.1",
        ],
    },
)
