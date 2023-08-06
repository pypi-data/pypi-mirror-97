#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

requirements = ['Click>=7.0', ] + required

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="CY Gatro",
    author_email='cragodn@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="DataAccess of quant app",
    entry_points={
        'console_scripts': [
            'cydb=cy_data_access.cli:cydb',
            'cyfin=cy_data_access.cli:cyfin',
            'cyusr=cy_data_access.user_cli:cyusr'
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='cy_data_access',
    name='cy_data_access',
    packages=find_packages(include=['cy_data_access', 'cy_data_access.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/cragod/CYDataAccess',
    version='0.4.20',
    zip_safe=False,
)
