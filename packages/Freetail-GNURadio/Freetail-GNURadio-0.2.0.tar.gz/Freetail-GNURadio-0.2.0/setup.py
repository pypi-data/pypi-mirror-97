from setuptools import setup
import os.path as osp

with open(osp.join('freetail_gnuradio', 'VERSION')) as version_file:
    version = version_file.read().strip()

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='Freetail-GNURadio',
    version=version,
    description='GNU Radio Blocks for the Freetail ultrasonic module',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/DavidPowell/Freetail-GNURadio',
    author='David A. Powell',
    author_email='david.powell@adfa.edu.au',
    packages=['freetail_gnuradio'],
    zip_safe=False,
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy',
        'pyserial',
    ],
    classifiers=[
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.8',
    ],
    package_data={
        'freetail_gnuradio': ['grc/*', 'VERSION'],
    },
)
