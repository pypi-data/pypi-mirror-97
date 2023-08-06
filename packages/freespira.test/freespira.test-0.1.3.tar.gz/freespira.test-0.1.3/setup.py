from setuptools import setup
from setuptools import find_packages

setup(
    name='freespira.test',
    version='0.1.3',
    description='test library for freespira code',
    author='Sean Reynolds and Paul Graham',
    author_email='sean@freespira.com, paul@freespira.com',
    install_requires=['pandas', 'numpy'],
    packages=find_packages(),
    zip_safe=False
)
