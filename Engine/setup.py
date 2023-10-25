from setuptools import setup, find_packages

setup(
    name='chess_engine',
    version='0.1',
    description='A brute force python chess engine.', 
    author='Frederick Andrews',  # Optional
    packages=find_packages(exclude=['Assets', 'unit_tests']),  # Required
    python_requires='>=3.6',
)
