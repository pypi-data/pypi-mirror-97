# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This uses the template https://github.com/pypa/sampleproject/blob/master/setup.py
# and from Alex Afanasyev's file at https://github.com/cawka/PyNDN2/blob/master/setup.py

# To build/upload the package, do the following as described in
# https://python-packaging-user-guide.readthedocs.org/en/latest/distributing.html
# sudo python3 setup.py sdist
# sudo python3 setup.py bdist_wheel --universal
# sudo python3 setup.py sdist bdist_wheel upload

from setuptools import setup, find_packages  # Always prefer setuptools over distutils

setup(
    name='PyNDN',

    version='2.13b1',

    description='An NDN client library with TLV wire format support in native Python',

    url='https://github.com/named-data/PyNDN2',

    maintainer='Jeff Thompson',
    maintainer_email='jefft0@remap.ucla.edu',

    license='LGPLv3',

    # See https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
    ],

    keywords='NDN',

    packages=find_packages('python'),
    package_dir={'': 'python'},

    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",

    install_requires=[
        'cryptography~=2.3',
        'mmh3~=2.5',
        'protobuf~=3.5',
        'trollius; python_version=="2.7"',
    ],

    extras_require={
        'doc': [
            'sphinx~=1.6.3',
        ],
        'test': [
            'pytest',
            'mock; python_version=="2.7"',
        ],
    }
)
