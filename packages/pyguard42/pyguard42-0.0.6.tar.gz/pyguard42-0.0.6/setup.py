from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pyguard42',
  version='0.0.6',
  entry_points = {
        'console_scripts': ['pyguard=pyguard.pyguard:main'],
  },
  project_urls = {
  'Github': 'https://www.github.com/kaankarakoc42/pyguard42'
  },
  description='auto-starter for python,javascript and cpp codes',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Mevlüt Kaan Karakoç',
  author_email='karakockaan326@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='auto-starter', 
  packages=find_packages(),
  install_requires=['keyboard','colorama'] 
)
