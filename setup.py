import pathlib
from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'Personal finance simulation package'

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Setting up
setup(
    name="pfinsim",
    version=VERSION,
    author="Xander Gerrmann",
    author_email="<xander@xgerrmann.com>",
    url='https://github.com/xgerrmann/pfinsim',
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    packages=['pfinsim'],
    install_requires=[
        'PyYAML>=5.3.1'
    ],
    keywords=['python', 'simulation', 'finance', 'personal'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    python_requires='>=3.7',
)
