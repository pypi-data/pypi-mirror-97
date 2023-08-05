import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='simpleemail',
    version='0.4',
    packages=['simpleemail'],
    url='https://github.com/N-C-C/SimpleEmail',
    license='MIT',
    author='John Glasgow',
    author_email='jglasgow@northampton.edu',
    description="Simple SMTP wrapper for Python's SMTP, supports both HTML and text based emails. Now supports attachments!",
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Communications :: Email",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython"
    ],
)
