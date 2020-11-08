#!/usr/bin/env python3
from distutils.core import setup

setup(name='rs232server',
      version='0.3',
      description='rs232 control of appliances',
      author='Brendan Le Foll',
      author_email='brendan@fridu.org',
      url='http://github.com/arfoll/rs232server',
      packages=['rs232modules'],
      scripts=['rs232server']
     )
