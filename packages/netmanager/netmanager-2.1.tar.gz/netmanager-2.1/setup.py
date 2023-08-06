import setuptools


with open("README.md") as readme:
    long_description = readme.read()


setuptools.setup(name='netmanager',
                 version='2.1',
                 description='Author: Danila Kisluk',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 packages=['netmanager'],
                 author_email='dankis12a@gmail.com')
