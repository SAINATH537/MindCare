# Setup script for packaging
# setup.py

from setuptools import setup, find_packages

setup(
    name="MentalHealthApp",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "tk",
        "matplotlib"
    ],
    entry_points={
        "console_scripts": [
            "mentalhealthapp = src.app:main"
        ]
    },
)