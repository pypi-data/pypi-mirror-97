
from setuptools import setup, find_packages
 
classifiers = [
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
	]
 
setup(
  name='Tklighter',
  version='0.0.1',
  description='Adds syntaxhighlighing to tkinter Text',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/Rogers-Kabuye0/TKlighter.git',  
  author='Rogers Kabuye',
  author_email='rogerskabuye0@gmail.com',
  license='Apache License', 
  classifiers=classifiers,
  keywords='_h', 
  packages=find_packages(),
  install_requires=[''] 
)