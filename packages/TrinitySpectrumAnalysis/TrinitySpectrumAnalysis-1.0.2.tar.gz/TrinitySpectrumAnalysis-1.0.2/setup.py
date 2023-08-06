import setuptools
from distutils.core import setup
from setuptools import setup, find_packages



setup(
    name='TrinitySpectrumAnalysis',
    version='1.0.2',
    author= 'Cade Rodgers',
    author_email="<cader@live.unc.edu>",
    packages=find_packages(),
    url= 'https://github.com/Cademan10/Trinity',
    install_requires=[
          'numpy',
          'PyQt5',
          'pyqtgraph',
          'numpy',
          'matplotlib',
          'scipy',
          'rpy2',
      ],
    include_package_data=True,
    package_data={'':['*.txt'],
                  '':['*.dat'],
                  '':['*.png']},
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)

