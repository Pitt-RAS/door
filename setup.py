"""Setup door package."""

from setuptools import setup, find_packages

setup(
    name="door",
    version="0.0.1",
    description="Door opener",
    packages=find_packages(),
    install_requires=[
        "pyserial",
        "slackclient",
    ],
    extras_require={
        "test": ["pytest", "pydocstyle", "flake8", "mypy"],
    },
    entry_points={
        "console_scripts": [
            "door=door.cli:cli",
        ],
    },
)
