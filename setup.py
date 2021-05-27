from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pytorreq',
      version='0.2.2',
      description='A simple python library that allows you to forward requests through the tor network',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/Exordio/pyTorReq',
      author='Ivan Golubev',
      author_email='exordio@gmail.com',
      license='MIT',
      py_modules=['pytorreq'],
      install_requires=[
          'PySocks>=1.5.7',
          'requests>=2.25.1',
          'stem>=1.8.0'
      ],
      zip_safe=False)
