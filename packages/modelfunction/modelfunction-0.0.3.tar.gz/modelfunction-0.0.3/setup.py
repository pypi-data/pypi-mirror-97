from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='modelfunction',
  version='0.0.3',
  description='Extract model function',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Suheda Seyhan',
  author_email='suhedaseyhan@hotmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='model', 
  packages=find_packages(),
  install_requires=[''] 
)