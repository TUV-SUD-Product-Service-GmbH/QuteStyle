from setuptools import setup

from tsl.version import VERSION

setup(name='tsl',
      version=VERSION,
      description='Library for TSL shared functions',
      url='https://tfs.itgr.net/TPS/TSL/_dashboards',
      author='Walid Amokrane, Tilman Krummeck',
      author_email='PS-TF-Entwicklung@tuev-sued.de',
      license='MIT',
      packages=['tsl'],
      zip_safe=False)
