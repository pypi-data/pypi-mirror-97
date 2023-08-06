#!/usr/bin/env

from setuptools import setup

setup(
    name='django-db-storage2',
    version='2.0.2.1',
    url='https://github.com/hitman711/django-db-storage',
    license='BSD',
    author='Siddhesh Gore',
    author_email='sidh711@gmail.com',
    description='Custom Database Storage for Django',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='django metrics analytics',
    packages=[
        'dbstorage',
        'dbstorage.migrations',
    ],
    include_package_data=True,
    zip_safe=False
)
