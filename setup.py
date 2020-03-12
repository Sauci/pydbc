from setuptools import setup

setup(
    name='sauci-pydbc',
    version='0.1.2',
    packages=[
        'pydbc.parser'
    ],
    license='BSD',
    author='Guillaume Sottas',
    url='https://github.com/Sauci/pydbc',
    author_email='guillaume.sottas@liebherr.com',
    description='utility for dbc files',
    long_description='this package provides an API to access different nodes in a dbc file',
    install_requires=[
        'ply'
    ],
    test_suite='tests',
    tests_require=[
        'pytest'
    ]
)
