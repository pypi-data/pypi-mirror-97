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
    install_requires= ['matplotlib>=3.0,<4.0','numpy >=1.0,<2.0','astropy>=4.0,<5.0','opencv-python >=4.0,<5.0','scikit-image>=0.16.2,<1.0','scipy>=1.0,<2.0','Pillow >=7.0,<8.0'],
    version='10',
    description='paquete de prueba prueba_ifsUW',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NildaX/python-prueba_ifsUW',
    author='F. Rosales Ortge,Anahi Nilda G.Xolo  Tlapanco',
    author_email='nilda_gaby_9745@live.com.mx',
    license='MIT',
    classifiers=['Programming Language :: Python :: 3.4'], 
    keywords=['testing', 'IFS', 'example'],
)