"""build configuration for the reusable maze generator package."""

from setuptools import setup

setup(
    name="mazegen",
    version="1.0.0",
    description="Reusable maze generator for the 42 A-Maze-ing activity",
    packages=["maze_generator"],
    python_requires=">=3.10",
    install_requires=["pydantic"],
    extras_require={"dev": ["flake8", "mypy", "wheel"]},
)
