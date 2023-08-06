import setuptools
import pathlib

here = pathlib.Path(__file__).parent
metadata = {}

with open(here / 'webspinner' / '__version__.py', encoding='utf-8') as f:
    exec(f.read(), metadata)

with open(here / 'README.md', encoding='utf-8') as f:
    readme = f.read()

setuptools.setup(
    name=metadata['__title__'],
    version=metadata['__version__'],
    author=metadata['__author__'],
    author_email=metadata['__author_email__'],
    description=metadata['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    url=metadata['__url__'],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    package_data={
        '': ['LICENSE']
    },
    install_requires=[
        'sqlalchemy'
    ],
    extras_require={
        'aws': [
            'pyathena',
            'awscli'
        ],
        'pgres': [
            'pgpasslib',
            'psycopg2'
        ],
        'parquet': [
            'pyarrow'
        ],
        'dev': [
            'twine',
            'setuptools',
            'wheel'
        ]
    },
    license='BSD-3',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ]
)
