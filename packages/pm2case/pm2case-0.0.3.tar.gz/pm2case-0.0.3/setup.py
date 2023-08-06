#encoding: utf-8
import io

from postman2case import __version__
from setuptools import find_packages, setup

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pm2case',
    version=__version__,
    description='Convert POSTMAN data to JSON testcases for HttpRunner.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Optional (see note above)
    author='luguo',
    author_email='hluguoj@163.com',
    url='https://github.com/HttpRunner/postman2case',
    license='MIT',
    packages=find_packages(exclude=['test.*', 'test']),
    package_data={},
    keywords='postman converter json',
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    entry_points={
        'console_scripts': [
            'pm2case=postman2case.cli:main'
        ]
    }
)
