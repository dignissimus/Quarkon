"""Quarkon, Quantum simulator

see: https://github.com/dignissimus/Quarkon
"""
from setuptools import setup, find_packages

setup(
    name="Quarkon",
    version="0.1.0",
    python_requires=">=3.6",
    description="Quantum circuit simulator",
    long_description="Quantum circuit simulator",
    url="https://github.com/dignissimus/Quarkon",
    author="Sam Ezeh",
    author_email="sam@ezeh.me",
    entry_points={
        "console_scripts": [
            "qasm = qasm.__main__:main"
        ]
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
)
