#!/usr/bin/env python

from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='eventy',
        version='2.5.2',
        url='https://github.com/qotto/eventy',
        license='MIT',
        author='Alexandre Syenchuk',
        author_email='sacha@qotto.net',
        description='Qotto/eventy',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'avro-python3',
            'pyyaml>=4.2b1',
            'aiokafka==0.5.2',
            'sanic'
        ],
        classifiers=[
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3.8',
        ],
    )
