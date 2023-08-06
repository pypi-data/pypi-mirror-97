import setuptools
import re

about = {}
with open('twseia/__version__.py') as fh:
    for line in fh.readlines():
        about.update(dict(re.findall('__([a-z]+)__ *= *\'([^"]+)\'', line)))

setuptools.setup(
    name=about.get('title'),
    version=about.get('version'),
    description=about.get('description'),
    author=about.get('author'),
    author_email=about.get('author_email'),
    url=about.get('url'),
    license=about.get('license'),
    packages=['twseia'],
    install_requires=['pyserial'],
    classifier=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
