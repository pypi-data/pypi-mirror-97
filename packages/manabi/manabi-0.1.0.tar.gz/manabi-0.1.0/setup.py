# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manabi']

package_data = \
{'': ['*'], 'manabi': ['data/*']}

install_requires = \
['WsgiDAV>=3.1.0,<4.0.0',
 'attrs>=20.3.0,<21.0.0',
 'pybase62>=0.4.3,<0.5.0',
 'pybranca>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'manabi',
    'version': '0.1.0',
    'description': 'Provide WebDAV access for documents.',
    'long_description': 'Manabi\n======\n\nInstall\n-------\n\nMake sure libsodium exists on the system, for example execute:\n\n```bash\napk add --no-cache libsodium\napt-get install -y libsodium23\n```\n\nDev\n===\n\nCurrently wsgidav is broken for python 3.8+.\n\nEnable dev-env:\n\n```bash\npyenv install 3.7.10\npoetry env use $HOME/.pyenv/versions/3.7.10/bin/python3.7\npoetry install\npoetry shell\n```\n\nConfig\n------\n\nCall `manabi-keygen` and add the key to `config["manabi"]["key"]`. The key is\nshared between the caluma/alexandria backend and the WebDAV server.\n\nmount_path\n: prefix that gets passed to wsgidav, if URL rewrites remove any prefixes use\n`"/"`\n\nlock_manager\n: The ManabiLockLockStorage forces the WebDav log-timeout to \n`token-refresh-time / 2`\n\nprovider_mapping\n: Extends the FilesystemProvider any will only serve files if the token is valid\n\nmiddleware_stack\n: based on the default middleware_stack but HTTPAuthenticator is replace by\nManabiAuthenticator, which validates the tokens.\n\nmanabi.key\n: shared-key between the server that creates tokens to grant access and wsgi-dav\n\nmanabi.refresh\n: how often tokens are refreshed in seconds, we recommend 10 minutes: `600`\n\nmanabi.initial\n: the time from the token being generated till it has to be refreshed the first\ntime, we recommend 1 minues: `60`. In case tokens leak, for example via cache on\na computer, tokens should be expired by the time an adversary gets them.\n\n```python\nconfig = {\n    "mount_path": "/dav",\n    "lock_manager": ManabiLockLockStorage(refresh),\n    "provider_mapping": {\n        "/": ManabiProvider(settings.MEDIA_ROOT),\n    },\n    "middleware_stack": [\n        WsgiDavDebugFilter,\n        ErrorPrinter,\n        ManabiAuthenticator,\n        WsgiDavDirBrowser,\n        RequestResolver,\n    ],\n    "manabi": {\n        "key": key,\n        "refresh": refresh,\n        "initial": settings.MANABI_TOKEN_ACTIVATE_TIMEOUT,\n    },\n}\n```\n\ngitlab\n======\n\nWe have switched to github-workflows, but the gitlab-ci is still inplace.\n\nWhen changing dependencies or the build image, ie any of these files:\n\n* c/build\n* c/install\n* c/pipinstall\n* Dockerfile\n* Pipfile\n* Pipfile.lock\n* setup.cfg\n* setup.py\n* MANIFEST.in\n\nYou need to merge the changes to master first, because the container can only be\npublished by a master build.\n\n!! Do not forget to increment MANABI_IMAGE_VERSION in ./c/config\n\nRelease notes\n=============\n\n0.2\n---\n\n* ManabiLockLockStorage takes `storage: Path` as argument, pointing to the\n  shared lock-storage. ManabiLockLockStorage will store the locks as\n  sqlite-database. In the future we might use memcache or some other method.\n\n* Users should add\n\n```python\n    "hotfixes": {\n        "re_encode_path_info": False,\n    },\n```\n\nto their config, as this workaround is not correct on webservers that work\ncorrectly. I we have tested this extensively with cherrypy.\n',
    'author': 'Adfinis AG',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/projectcaluma/manabi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<3.8',
}


setup(**setup_kwargs)
