from setuptools import setup

setup(name='pytorreq',
  version='0.1.0',
  description='A simple python library that allows you to forward requests through the tor network',
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