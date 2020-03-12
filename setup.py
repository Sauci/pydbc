from setuptools import setup

setup(
    name='sauci-pydbc',
    version='0.1.0',
    packages=[
        'pydbc',
        'pydbc.parser'
    ],
    license='BSD',
    author='Guillaume Sottas',
    url='https://github.com/Sauci/pydbc',
    author_email='guillaume.sottas@liebherr.com',
    description='utility for dbc files',
    entry_points={
        'console_scripts': [ 'pya2l=pya2l:main' ]
    },
    long_description='this package provides an API to access different nodes in a dbc file',
    install_requires=[
        'ply'
    ],
    dependency_links=[
        'https://pypi.python.org/packages/e5/69/882ee5c9d017149285cab114ebeab373308ef0f874fcdac9beb90e0ac4da/ply-3.11.tar.gz#md5=6465f602e656455affcd7c5734c638f8'
    ]
)
