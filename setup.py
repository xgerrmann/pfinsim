from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Personal finance simulation package'
LONG_DESCRIPTION = 'Package containing tools for analysing and simulating ones personal financial situation'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="pfinsim",
    version=VERSION,
    author="Xander Gerrmann",
    author_email="<xander@xgerrmann.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'simulation', 'finance', 'personal'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ]
)
