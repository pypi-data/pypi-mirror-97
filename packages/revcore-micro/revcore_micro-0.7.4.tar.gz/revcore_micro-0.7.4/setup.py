from distutils.core import setup
from revcore_micro import __version__
from setuptools import find_packages

setup(
    name='revcore_micro',
    version=__version__,
    license='MIT',
    description='service core for revteltech',
    author='Chien Hsiao',
    author_email='chien.hsiao@revteltech.com',
    keywords=['revteltech', 'micro service'],
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'boto3',
        'jwcrypto',
        'pyjwt',
        'marshmallow'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
