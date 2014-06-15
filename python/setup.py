import sys
from setuptools import setup

# Ref: http://semver.org/
with open("VERSION", "rt") as in_file:
    VERSION = in_file.read().strip()

AUTHOR='Nathan Farrington'
AUTHOR_EMAIL='nathan@nathanfarrington.com'
CLASSIFIERS=[
    'Development Status :: 4 - Beta',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Object Brokering',
    'Topic :: System :: Distributed Computing'
]
DESCRIPTION='Lightweight RPC using Redis'
DOWNLOAD_URL='https://github.com/downloads/nfarring/redisrpc/redisrpc-python-%s.tar.gz' % VERSION
INSTALL_REQUIRES=[
    'distribute',
    'redis',
]
KEYWORDS=['Redis','RPC']
with open('README.rst','r') as f:
    LONG_DESCRIPTION=''.join(f.readlines())
MAINTAINER=AUTHOR
MAINTAINER_EMAIL=AUTHOR_EMAIL
NAME='redisrpc'
PY_MODULES=['redisrpc']
TESTS_REQUIRE=[
    'pytest',
    'pytest-dbfixtures',
    'tox',
]
URL='http://github.com/nfarring/redisrpc'

setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=CLASSIFIERS,
    description=DESCRIPTION,
    download_url=DOWNLOAD_URL,
    install_requires=INSTALL_REQUIRES,
    keywords=KEYWORDS,
    long_description=LONG_DESCRIPTION,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    name=NAME,
    py_modules=PY_MODULES,
    tests_require=TESTS_REQUIRE,
    url=URL,
    version=VERSION
)
