from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'GBM Client Library for Python'
LONG_DESCRIPTION = 'This is a client library for the mexican broker GBM(grupo bursatil mexicano) meant to run alongside with trading algoritms'

# Setting up
setup(
    name="GBMProyect",
    version="0.0.2",
    author="Jason Dsouza",
    author_email="raul.sosa.cortes@gmail.com",
    description='GBM Client Library for Python',
    long_description='This is a client library for the mexican broker GBM(grupo bursatil mexicano) meant to run alongside with trading algoritms',
    packages=find_packages(),
    install_requires=['pytz', 'requests'],
    keywords=['python', 'GBM', 'AlgoTrading'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent"
    ]
)