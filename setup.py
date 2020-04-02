# -*- coding: utf-8 -*-
__revision__ = "$Id$"

from setuptools import setup, find_packages
import os
import sys
from os.path import join as pj


from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key, value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))


# compile cython code
cwd = os.getcwd()
os.chdir('src/openalea/stocatree')
os.system('python build_cython.py')
os.chdir(cwd)

if __name__ == '__main__':

    setup(name=name,
          version=version,
          author=authors,
          author_email=authors_email,
          description=description,
          url=url,
          license=license,

          # Packages
          packages=['openalea',
                    'openalea.stocatree',
                    'openalea.stocatree.tools',
                    'openalea.stocatree_wralea',
                    'openalea.stocatree_configuration_wralea'],

          package_dir={
              '': 'src',
              'openalea': 'src/openalea',
              'openalea.stocatree': 'src/openalea/stocatree',
              'openalea.stocatree_wralea': 'src/openalea/stocatree_wralea',
              'openalea.stocatree_configuration_wralea': 'src/openalea/stocatree_configuration_wralea'},

          package_data={'': ['*.lpy', '*.fset',
                             '*.s', '*.txt', '*pyd', '*.so'], },
          include_package_data=True,
          share_dirs={'share': 'share'},
          # Add package platform libraries if any
          zip_safe=False,

          # Dependencies
          #install_requires = ['vplants.plantgl', 'cython', 'lockfile'],
          dependency_links=['http://openalea.gforge.inria.fr/pi'],
          # cmdclass={'build_ext':build_ext},
          #ext_modules = ext_modules,

          entry_points={
              "wralea": ["openalea.stocatree = openalea.stocatree_wralea",
                         "openalea.stocatree.configuration = openalea.stocatree_configuration_wralea",
                         ]
          },



          )
