import os

from setuptools import setup


def read(fname):
    absolute_fname = os.path.join(os.path.dirname(__file__), fname)
    with open(absolute_fname, 'r') as fp:
        return fp.read()


setup(
    name='flatbencode',
    version='0.2.0',
    author="Antoine Catton",
    description="Fast, safe and non-recursive implementation of Bittorrent bencoding for Python 3",
    long_description=read('README.rst'),
    license='MIT',
    keywords="bencoding bencode bittorrent fast non-recursive stack maximum recursion",
    url='http://github.com/acatton/flatbencode',
    py_modules=['flatbencode'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: File Sharing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
