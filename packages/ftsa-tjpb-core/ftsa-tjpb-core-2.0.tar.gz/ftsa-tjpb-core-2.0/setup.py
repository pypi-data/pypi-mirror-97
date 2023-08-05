import io
from setuptools import setup, find_packages
from ftsa.core.properties import VERSION, PACKAGE_NAME, FTSA_DATABASE_LIB_NAME, \
    FTSA_SELENIUM_LIB_NAME, FTSA_SSH_LIB_NAME, FTSA_APPIUM_LIB_NAME, FTSA_REQUESTS_LIB_NAME

with io.open('README.md', 'r', encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author='Carlos Diego Quirino Lima',
    author_email='diegoquirino@gmail.com',
    description='Framework de Teste de Sistemas Automatizado - CORE',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://gitlab-novo.tjpb.jus.br/testes/ftsa/core',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords=f'ftsa framework teste sistemas e2e automatizado tjpb core '
             f'{FTSA_DATABASE_LIB_NAME} {FTSA_SELENIUM_LIB_NAME} {FTSA_SSH_LIB_NAME} {FTSA_APPIUM_LIB_NAME}'
             f'{FTSA_REQUESTS_LIB_NAME}',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'robotframework',
        'robotframework-seleniumlibrary',
        'robotframework-sshlibrary',
        'robotframework-databaselibrary',
        'robotframework-appiumlibrary',
        'robotframework-requests',
        'robotframework-faker',
        'webdrivermanager',
        'selenium'
    ],
    platforms='windows linux mac',
)
