import os
from setuptools import setup

setup(
    name='hdfscontents',
    version='0.8',
    author='Ahmad Al-Shishtawy',
    author_email='alshishtawy@gmail.com',
    description='Jupyter content manager that uses the HDFS filesystem',
    license='Apache License 2.0',
    keywords='Jupyter, HDFS, HOPS, Hadoop',
    url='https://github.com/hopshadoop/hdfscontents',
    download_url = 'https://github.com/hopshadoop/hdfscontents/archive/0.6.tar.gz',
    packages=['hdfscontents', 'tests'],
    long_description='A contents manager for Jupyter that uses the Hadoop File System (HDFS) to store Notebooks and files',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: IPython',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ], install_requires=['traitlets', 'notebook', 'pydoop', 'tornado', 'nbformat', 'ipython_genutils']
)
