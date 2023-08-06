
from setuptools import setup, Extension

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'kvdroid',
    packages = ['.'],
    version = '0.1.1',
    description = 'Some Android tools for Kivy developments',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'Yunus Ceyhan',
    author_email = 'yunus.ceyhn@gmail.com',
    url = 'https://github.com/yunus-ceyhan/kvdroid.git',
    keywords = ['Android', 'Python','Kivy'],
    install_requires=["kivy"],
    classifiers = [],
)