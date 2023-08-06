from setuptools import find_packages, setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='ocdsextensionregistry',
    version='0.1.3',
    author='Open Contracting Partnership',
    author_email='data@open-contracting.org',
    url='https://github.com/open-contracting/extension_registry.py',
    description="Eases access to information from the extension registry of the Open Contracting Data Standard",
    license='BSD',
    packages=find_packages(exclude=['tests', 'tests.*']),
    long_description=long_description,
    install_requires=[
        'json-merge-patch',
        'jsonref',
        'requests',
        'requests-cache',
    ],
    extras_require={
        'test': [
            'pytest',
        ],
        'docs': [
            'Sphinx',
            'sphinx-autobuild',
            'sphinx_rtd_theme',
        ],
        'cli': [
            'Babel',
            'MyST-Parser',
            'ocds-babel[markdown]>=0.3.0',
            'Sphinx',
        ]
    },
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'ocdsextensionregistry = ocdsextensionregistry.cli.__main__:main',
        ],
    },
)
