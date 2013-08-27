#!/usr/bin/env python
# coding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='tornado_msgpack',
        version=0.2,
        author='ousttrue',
        author_email='ousttrue@gmail.com',
        description="ore ore MessagePack RPC",
        long_description=open('README.rst').read(),
        packages=['tornado_msgpack'],
        install_requires=['msgpack-python', 'tornado'],
        license="Apache Software License",
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: Apache Software License'],
)
