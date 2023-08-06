# -*- coding: utf-8 -*-
from distutils.core import setup
import setuptools

with open('./version.txt', encoding='utf8') as f:
    version = f.read().strip()

with open('./README.md', 'r', encoding='utf8') as f:
    long_description = f.read()

with open('./requirements.txt', 'r', encoding='utf8') as f:
    install_requires = list(map(lambda x: x.strip(), f.readlines()))
print(setuptools.find_packages())
setup(
    name='lightNLU',
    version=version,
    description="A lightweight natural language understanding library",
    author='lightsmile',
    author_email='iamlightsmile@gmail.com',
    url='https://github.com/smilelight/lightNLU',
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
)
