from setuptools import setup, find_packages
from integration_utils import __version__

setup(
    name='smart-integration-utils',
    version=__version__,
    packages=find_packages(),
    setup_requires=['Django>=2.2.7', 'djangorestframework>=3.8.2', 'requests>=2.18.2',],
    install_requires=[
        'psycopg2-binary>=2.7.4',
        'pytz>=2018.4',
        'six>=1.11.0',
        'config_field',
        'drf-dynamicfieldserializer',
        'pycrypto==2.6.1',
    ],
    python_requires='>=3.7',
)
