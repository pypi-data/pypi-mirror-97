"""Setup script for naive-tester package"""
import os.path
from setuptools import setup


HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'README.md')) as file:
    README = file.read()

setup(
    name='naive-tester',
    version='1.2.1',
    description='A simple testing system based on files',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/FilippSolovev/naive-tester',
    author='Filipp Solovev',
    author_email='solovyev.filipp@gmail.com',
    licence='MIT',
    packages=['tester'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
    entry_points={"console_scripts": ["tester=tester.__main__:main"]},
)
