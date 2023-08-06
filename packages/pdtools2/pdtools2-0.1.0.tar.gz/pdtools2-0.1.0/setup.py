from setuptools import setup, find_packages

setup(
    author = "Masum Rumi",
    description = "A package that helps reduce memory usage when working with pandas",
    name = "pdtools2",
    version = "0.1.0",
    packages = find_packages(include=["pdtools2", "pdtools2.*"]),
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.0'
    ],
    python_requires='>=3.8'



)