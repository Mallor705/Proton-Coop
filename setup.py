# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="multiscope",
    version="0.5.0",
    description="A tool to launch multiple instances of Steam using Gamescope.",
    author="Jules",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "psutil>=5.9.0",
        "pydantic>=2.0.0",
        "PyGObject>=3.42.0",
    ],
    entry_points={
        "gui_scripts": [
            "multiscope=multiscope:main",
        ]
    },
)
