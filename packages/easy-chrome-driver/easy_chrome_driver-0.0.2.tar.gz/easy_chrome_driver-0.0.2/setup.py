"""
Your licence goes here
"""
 
from setuptools import setup, find_packages
 
# See note below for more information about classifiers
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: POSIX :: Linux',
  'Operating System :: Microsoft :: Windows',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='easy_chrome_driver',
  version='0.0.2',
  description='Abstraction for chrome driver for easy modifications',
  long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/vaibhavkpatel1/easy_chrome_driver',  # the URL of your package's home page e.g. github link
  author='Vaibhavkumar Patel',
  author_email='vaibhavkpatel1@gmail.com',
  license='MIT', # note the American spelling
  classifiers=classifiers,
  keywords='easy_chromedriver chrome_driver webdriver proxy_driver', # used when people are searching for a module, keywords separated with a space
  packages=find_packages(),
  install_requires= open('requirements.txt','r').readlines() # a list of other Python modules which this module depends on.  For example RPi.GPIO
)
