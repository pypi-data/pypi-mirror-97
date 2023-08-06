# -*- coding: utf8 -*-

from setuptools import setup, find_packages

with open("README.md") as fh:
    long_description = fh.read()

setup(
    # Basic info
    name="perf-py",
    version="0.0.1",
    author='Omar Eid',
    author_email='contact.omar.eid@gmail.com',
    url='https://github.com/mr-uuid/perfpy',
    description='Understanding performance characteristics of common python constructs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    # Packages and depencies
    packages=find_packages(),
    install_requires=[
        "attrs",
        "pydantic",
        "toolz",  # https://toolz.readthedocs.io/en/latest/api.html
        "numpy"
        # 'jinja2',
        # 'invoke>=0.13',
        # 'unidecode',
        # 'six',
    ],
    extras_require={
        'dev': [
            # "nbconvert==5.5.0",
            "ipython",
            "mypy",
            "pytest",
            "pytest-pep8",
            "pytest-profiling",  # https://pypi.org/project/pytest-profiling/
            "pstats-view",  # https://github.com/ssanderson/pstats-view
            "flake8",
            # 'manuel',
            # 'pytest-cov',
            # 'coverage',
            # 'mock',
        ],
    },
    # Data files
    package_data={},
    # Scripts
    entry_points={
        'console_scripts': [
            'python-boilerplate = python_boilerplate.__main__:main'],
    },
    # Other configurations
    zip_safe=False,
    platforms='any'
)
