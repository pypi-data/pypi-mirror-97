from setuptools import setup, find_packages

import lazyvpn

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='lazyvpn',
    version=lazyvpn.version,
    install_requires=requirements,
    author='Yuzhong Li, Clayton Blythe',
    author_email='yuzhongl@zillowgroup.com, claytonb@zillowgroup.com',
    description="A CLI to connect to vpn via cisco anyconnect in one step",
    url='https://github.com/lyzh945/lazyvpn',
    license='Apache License, v2.0',
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite="tests",
    scripts=['bin/lazyvpn', 'bin/lazyvpn.cmd'],
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: Apache Software License'
    ]
)
