# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nio',
 'nio.client',
 'nio.crypto',
 'nio.event_builders',
 'nio.events',
 'nio.store']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.4.0,<0.5.0',
 'aiohttp-socks>=0.5.5,<0.6.0',
 'aiohttp>=3.6.2,<4.0.0',
 'future>=0.18.2,<0.19.0',
 'h11>=0.9.0,<0.10.0',
 'h2>=3.2.0,<4.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'logbook>=1.5.3,<2.0.0',
 'pycryptodome>=3.9.7,<4.0.0',
 'unpaddedbase64>=1.1.0,<2.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 'e2e': ['python-olm>=3.1.3,<4.0.0',
         'peewee>=3.13.2,<4.0.0',
         'cachetools>=4.0.0,<5.0.0',
         'atomicwrites>=1.3.0,<2.0.0']}

setup_kwargs = {
    'name': 'matrix-nio',
    'version': '0.17.0',
    'description': 'A Python Matrix client library, designed according to sans I/O principles.',
    'long_description': 'nio\n===\n\n[![Build Status](https://img.shields.io/github/workflow/status/poljar/matrix-nio/Build%20Status?style=flat-square)](https://github.com/poljar/matrix-nio/actions)\n[![codecov](https://img.shields.io/codecov/c/github/poljar/matrix-nio/master.svg?style=flat-square)](https://codecov.io/gh/poljar/matrix-nio)\n[![license](https://img.shields.io/badge/license-ISC-blue.svg?style=flat-square)](https://github.com/poljar/matrix-nio/blob/master/LICENSE.md)\n[![Documentation Status](https://readthedocs.org/projects/matrix-nio/badge/?version=latest&style=flat-square)](https://matrix-nio.readthedocs.io/en/latest/?badge=latest)\n[![#nio](https://img.shields.io/badge/matrix-%23nio:matrix.org-blue.svg?style=flat-square)](https://matrix.to/#/!JiiOHXrIUCtcOJsZCa:matrix.org?via=matrix.org&via=maunium.net&via=t2l.io)\n\nnio is a multilayered [Matrix](https://matrix.org/) client library. The\nunderlying base layer doesn\'t do any network IO on its own, but on top of that\nis a full fledged batteries-included asyncio layer using\n[aiohttp](https://github.com/aio-libs/aiohttp/). File IO is only done if you\nenable end-to-end encryption (E2EE).\n\nDocumentation\n-------------\n\nThe full API documentation for nio can be found at\n[https://matrix-nio.readthedocs.io](https://matrix-nio.readthedocs.io/en/latest/#api-documentation)\n\nFeatures\n--------\n\nnio has most of the features you\'d expect in a Matrix library, but it\'s still a work in progress.\n\n- ✅ transparent end-to-end encryption (EE2E)\n- ✅ encrypted file uploads & downloads\n- ✅ manual and emoji verification\n- ✅ custom [authentication types](https://matrix.org/docs/spec/client_server/r0.6.0#id183)\n- ✅ well-integrated type system\n- ✅ kick, ban and unban\n- ✅ typing notifications\n- ✅ message redaction\n- ✅ token based login\n- ✅ user registration\n- ✅ read receipts\n- ✅ live syncing\n- ✅ `m.tag`s\n- ❌ python 2.7 support\n- ❌ cross-signing support\n- ❌ user deactivation ([#112](https://github.com/poljar/matrix-nio/issues/112))\n- ❌ in-room emoji verification\n- ❌ room upgrades and `m.room.tombstone` events ([#47](https://github.com/poljar/matrix-nio/issues/47))\n\nInstallation\n------------\n\nTo install nio, simply use pip:\n\n```bash\n$ pip install matrix-nio\n\n```\n\nNote that this installs nio without end-to-end encryption support. For e2ee\nsupport, python-olm is needed which requires the\n[libolm](https://gitlab.matrix.org/matrix-org/olm) C library (version 3.x).\nOn Debian and Ubuntu one can use `apt-get` to install package `libolm-dev`.\nOn Fedora one can use `dnf` to install package `libolm-devel`.\nOn MacOS one can use [brew](https://brew.sh/) to install package `libolm`.\nMake sure version 3 is installed.\n\nAfter libolm has been installed, the e2ee enabled version of nio can be\ninstalled using pip:\n\n```bash\n$ pip install "matrix-nio[e2e]"\n\n```\n\nAdditionally, a docker image with the e2ee enabled version of nio is provided in\nthe `docker/` directory.\n\nExamples\n--------\n\nFor examples of how to use nio, and how others are using it,\n[read the docs](https://matrix-nio.readthedocs.io/en/latest/examples.html)\n',
    'author': 'Damir Jelić',
    'author_email': 'poljar@termina.org.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/poljar/matrix-nio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
