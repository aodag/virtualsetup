from setuptools import setup, find_packages
import os

readme = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

setup(
    name="virtualsetup",
    version="0.0",
    author="Atsushi Odagiri",
    author_email="aodagx@gmail.com",
    license='MIT',
    url='https://github.com/aodag/flexenv',
    packages=find_packages(),
    description='manage eggs for virtalenv',
    long_description=readme,
    install_requires=['distribute'],
    test_suite='virtualsetup',
    entry_points={
        "console_scripts":[
            "virtualsetup=virtualsetup:main",
        ],
    },
)
