from setuptools import find_packages, setup
setup(
    name='c3loc',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.5.2',
    description='C3 Enhanced Proximity Location Services',
    url='https://gitlab.com/C3Wireless/c3loc',
    author='C3 Wireless',
    author_email='support@c3wireless.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='c3 c3wireless btle beacon ibeacon',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=[
        'alembic',
        'asyncpg',
        'aiohttp',
        'aiohttp-cors',
        'aiohttp-jinja2',
        'automat',
        'click',
        'marshmallow',
        'protobuf',
        'psycopg2',
        'python-lzo',
        'cryptography'
    ],
    extras_require={
        'test': ['tox']
    },
    entry_points={
        'console_scripts': [
            'c3loc_ingest=c3loc.ingest.main:main',
            'c3loc_api=c3loc.api.main:main',
        ],
    },
    package_data={'c3loc': ['static/*', 'templates/*', 'alembic.ini.local', 'alembic/*', 'alembic/versions/*']}
)
