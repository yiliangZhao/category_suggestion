from distutils.core import setup, Extension

setup(name='pytextproc',
    version='1.0',
    description="python textproc",
    packages=['textproc'],
    package_dir={'textproc':'textproc'},
    package_data={'textproc': ['textproc.so', 'textproc.h']})