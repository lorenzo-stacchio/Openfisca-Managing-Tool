#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='OpenFisca-Management-Tool',
    version='0.1.0',
    author='Lorenzo Stacchio and Corrado Petrelli in collaboration with OpenFisca Team',
    author_email='lorenzo.stacchio.dev@gmail.com, corrado.petrelli@gmail.com, contact@openfisca.fr',
    description=u'OpenFisca management tool for openfisca-country-package',
    keywords='management microsimulation tax benefit system reform',
    license='http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url='https://github.com/LorenzoStacchioDev/Openfisca-Manage-Tool',
    include_package_data = True,  # Will read MANIFEST.in
    install_requires=[
        'OpenFisca-Core >= 22.0, < 24.0',
        'Kivy >= 1.10.0',
        'Kivy-Garden >= 0.1.4',
        'kivy.deps.glew >= 0.1.9',
        'kivy.deps.gstreamer  >= 0.1.12',
        'python-dateutil >= 2.7'
        ],
    extras_require = {
        'api': [
            'OpenFisca-Web-API >= 4.0.0, < 7.0',
            ],
        'test': [
            'flake8 >= 3.4.0, < 3.5.0',
            'flake8-print',
            'nose',
            ]
        },
    packages=find_packages(),
    test_suite='nose.collector',
    )
