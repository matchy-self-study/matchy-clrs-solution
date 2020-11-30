from distutils.core import setup, Extension

module = Extension('hello', sources=['LRCS.c'])

setup(name = 'PackageName',
      version = '1.0',
      description='This is a test package',
      ext_modules= [module])
