# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:29:08 2021

@author: hp
"""
from setuptools import setup, find_packages
with open('README.md', 'r') as fh:
    long_description = fh.read()
setup(
    name='prueba_ifsUW',
    packages=find_packages(include=['prueba_ifsUW', 'prueba_ifsUW.*']),
    include_package_data = True,
    install_requires= ['matplotlib','numpy','astropy','opencv-python','scikit-image','scipy','Pillow'],
    version='4',
    description='paquete de prueba prueba_ifsUW',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NildaX/python-prueba_ifsER',
    author='Nilda G.Xolo  Tlapanco',
    author_email='nilda_gaby_9745@live.com.mx',
    license='MIT',
    classifiers=['Programming Language :: Python :: 3.4'], 
    keywords=['testing', 'IFS', 'example'],
)