from setuptools import setup, find_packages

setup(
    name="sorting_benchmark",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'dash',
        'pandas',
        'plotly',
        'python-dotenv'
    ]
) 