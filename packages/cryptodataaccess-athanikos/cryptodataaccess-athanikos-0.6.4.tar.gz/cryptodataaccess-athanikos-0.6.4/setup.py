import setuptools
from distutils.core import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cryptodataaccess-athanikos',
    version="0.6.4",
    license='MIT License',
    author='Nikos Athanasakis',
    packages=setuptools.find_packages(),
    author_email='athanikos@gmail.com',
    description='data access layer for crypto model  ',
    tests_require=['pytest'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
