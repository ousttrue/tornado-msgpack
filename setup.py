#!/usr/bin/env python
# coding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='tornado_msgpack',
        version=0.1,
        author='ousttrue',
        author_email='ousttrue@gmail.com',
        description="ore ore MessagePack RPC",
        long_description="""\
                MessagePack RPC for Python.

This implementation uses Tornado framework as a backend.
And it is not hide tornado.ioloop.
""",
        packages=['tornado_msgpack'],
        install_requires=['msgpack-python', 'tornado'],
        license="Apache Software License",
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: Apache Software License'],
)
