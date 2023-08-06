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
    install_requires= ['matplotlib>=3.2.2,<4.0.0','numpy >=1.18.5,<1.20.0','astropy>=4.0.1,<5.0.0','opencv-python >=4.4.0.46,<4.5.0.0','scikit-image>=0.16.2,<1.0.0.','scipy>=1.5.0,<2.0.0','Pillow >=7.2.0,<8.2.0'],
    version='7',
    description='paquete de prueba prueba_ifsUW',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NildaX/python-prueba_ifsUW',
    author='Nilda G.Xolo  Tlapanco',
    author_email='nilda_gaby_9745@live.com.mx',
    license='MIT',
    classifiers=['Programming Language :: Python :: 3.4'], 
    keywords=['testing', 'IFS', 'example'],
)