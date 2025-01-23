from setuptools import setup, find_packages

setup(
    name='cattax',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'celery',
        'django',
        'redis',
    ],
) 