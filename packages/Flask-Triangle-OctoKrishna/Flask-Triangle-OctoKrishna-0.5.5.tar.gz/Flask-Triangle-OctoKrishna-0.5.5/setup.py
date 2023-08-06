#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='Flask-Triangle-OctoKrishna',
    version='0.5.5',
    author='Krishna Y',
    author_email='webkrishna@outlook.com',
    description=('Integration of AngularJS and Flask, originally created by Morgan Delahaye-Prat (mdp@m-del.fr).'),
    long_description=open('README.rst').read(),
    packages=find_packages(),
    zip_safe=False,
    platforms='any',
    install_requires=['flask', 'jsonschema'],
    tests_require=['nose'],
    url='https://github.com/robinschoss/flask-triangle',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
