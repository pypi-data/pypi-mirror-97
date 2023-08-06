from setuptools import setup, find_packages

# -*- coding: utf-8 -*-
"""remote_edit module setup"""

setup(
    name='remote_edit',
    version='1.0.0',
    license='MIT',
    author='Shibani Mahapatra',
    author_email='shibani.mahapatra47@gmail.com',
    url='',
    description='',
    long_description='',
    long_description_content_type='text/markdown',
    keywords='remote code editor',
    packages=['remote_edit'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    entry_points={
        'console_scripts': [
            'remote_edit = remote_edit.RemoteEdit:main',
        ]
    },
    python_requires='>=2.7.0',
    install_requires=[
        'flaskcode==0.0.7',
        'pyngrok==4.2.2',
        'click>=5.1'

    ],

    classifiers=[

        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Text Editors :: Text Processing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)