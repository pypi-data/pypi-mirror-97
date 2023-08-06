'''
Copyright 2018-2021 Autograders

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import pathlib
import setuptools

# README.md
README = (pathlib.Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    license='MIT',
    name='autograders-cli',
    version='1.1.0',
    author='Andrés Castellanos',
    author_email='andres.cv@galileo.edu',
    description='Autograders Command Line Interface',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/autograders/cli/',
    project_urls={
        'Source': 'https://github.com/autograders/cli/',
        'Documentation': 'https://github.com/Autograders/cli/blob/main/README.md'
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    packages=[
        'autograder'
    ],
    python_requires='>=3.6',
    install_requires=[
        'certifi >= 2020.12.5',
        'chardet >= 4.0.0',
        'idna >= 2.10',
        'requests >= 2.25.1',
        'tabulate >= 0.8.7',
        'urllib3 >= 1.26.3',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'autograder = autograder.__main__:main'
        ]
    }
)
