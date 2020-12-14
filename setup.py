#!/usr/bin/python

from distutils.core import setup

setup(
    name = 'GrooveHQ',
    author = 'Matt Luongo',
    version = '0.1',
    author_email = 'mhluongo@gmail.com',
    packages = ['groovehq'],
    include_package_data = True,
    install_requires = ['requests'],
    license='LICENSE',
    url = 'https://github.com/cardforcoin/groovehq',
    keywords = 'groovehq groove api helpdesk',
    description = 'Python API Wrapper for GrooveHQ',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet'
    ],
)
