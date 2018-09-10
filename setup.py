from setuptools import setup, find_packages


setup(name='Tanks',
      packages=find_packages(),
      install_requires=[
          'nose',
          'coverage',
          'numpy',
          'pygame',
          'pytmx'
      ])