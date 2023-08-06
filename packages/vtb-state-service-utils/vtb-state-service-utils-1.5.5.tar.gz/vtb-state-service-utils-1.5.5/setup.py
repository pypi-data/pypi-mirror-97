from setuptools import setup, find_packages

"""
python setup.py sdist bdist_wheel
python -m twine upload --repository pypi dist/*
"""

REQUIRED = [
    'aiohttp>=3.6.2',
    'aio_pika>=6.6.1',
    'simplejson>=3.17.2',
    'vtb-py-logging>=1.0.4'
]

setup(
    name='vtb-state-service-utils',
    version='1.5.5',
    packages=find_packages(exclude=['tests']),
    url='https://bitbucket.org/Michail_Shutov/state_service_utils',
    license='',
    author=' Mikhail Shutov',
    author_email='michael-russ@yandex.ru',
    description='utils for VTB state service',
    install_requires=REQUIRED,
    extras_require={
        'test': [
            'pytest',
            'pytest-env',
            'pylint',
            'pytest-asyncio'
        ]
    }
)
