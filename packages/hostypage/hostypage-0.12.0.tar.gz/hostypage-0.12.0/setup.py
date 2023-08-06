import os
from setuptools import setup

version = os.environ.get('CI_COMMIT_TAG', '0.4')

with open('README.md') as f:
    long_description = f.read()

setup(
    name='hostypage',
    version=version,
    packages=['hosty'],
    author='Hosty.Page',
    author_email='christopherdavies553@gmail.com',
    description='CLI for Hosty.Page',
    scripts=['bin/hostypage'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['click==7.1.2', 'requests==2.25.1', 'progress==1.5'],
)
