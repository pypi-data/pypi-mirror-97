from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='spec_utils',
    version='0.11.0',
    description='SDKs to consume SPEC SA and third-party applications from Python',
    py_modules=['connectors',],
    packages=['spec_utils'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],

    long_description=long_description,
    long_description_content_type='text/markdown',

    install_requires=[
        'requests',
        'pandas',
        'sqlalchemy'
    ],

    extra_require={
        'dev': [
            'pytest>=3.8',
        ],
    },

    url='https://github.com/lucaslucyk/spec-utils',
    author='Lucas Lucyk',
    author_email='lucaslucyk@gmail.com',
)
