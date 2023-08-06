from setuptools import setup, find_packages

setup(
    name='freespira.test',
    version='0.1.0',
    description='test library for freespira code',
    author='Sean Reynolds and Paul Graham',
    author_email='sean@freespira.com, paul@freespira.com',
    instal_requires=[
        "pandas==1.2.1",
        "selenium==3.141.0",
        "matplotlib==3.3.3",
        "numpy==1.19.5"
    ],
    packages=find_packages()
)