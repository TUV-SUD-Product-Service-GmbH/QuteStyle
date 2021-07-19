from setuptools import setup

from tsl.version import VERSION

setup(name='tsl',
      version=VERSION,
      description='Library for TSL shared functions',
      url='https://tfs.itgr.net/TPS/TSL/_dashboards',
      author='Walid Amokrane, Tilman Krummeck',
      author_email='PS-TF-Entwicklung@tuev-sued.de',
      license='MIT',
      packages=['tsl', 'tsl.gen', 'tsl.dev', 'tsl.dev.test_procedures'],
      package_data={
            'tsl': ['py.typed'],
            'tsl.dev.test_procedures': ['SP_NAV_INSERT_PACKAGE.sql', 'SP_NAV_INSERT_PACKAGE_WITH_FILTER.sql']
      },
      install_requires=[
            'sqlalchemy',
            'pyodbc',
            'PyQt5'
      ],
      zip_safe=False)
