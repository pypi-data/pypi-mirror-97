#  Copyright 2021 Data Spree GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dlds-client',
    version='1.2.2',
    author="Data Spree GmbH",
    author_email="info@data-spree.com",
    url="https://data-spree.com/products/deep-learning-ds",
    license="Apache-2.0",
    description="Python API for Deep Learning DS from Data Spree.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'dlds.decoder'
    ],
    py_modules=[
        'dlds.dlds_cli',
        'dlds.dlds_client',
        'dlds.dlds_data_loader',
        'dlds.dlds_model',
        'dlds.dlds_worker',
        'dlds.http_token_authentication'
    ],
    install_requires=[
        'Click',
        'joblib',
        'requests',
        'tqdm',
    ],
    extras_require={
        'kitti': ['Pillow'],
        'worker': ['aiofiles', 'aiohttp', 'aiohttp_cors', 'Pillow']
    },
    entry_points='''
        [console_scripts]
        dlds=dlds.dlds_cli:cli
    ''',
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)
