# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unpaddedbase64']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unpaddedbase64',
    'version': '2.1.0',
    'description': 'Encode and decode Base64 without "=" padding',
    'long_description': 'Unpadded Base64\n===============\n\nEncode and decode Base64 without "=" padding.\n\n`RFC 4648`_ specifies that Base64 should be padded to a multiple of 4 bytes\nusing "=" characters. However many protocols choose to omit the "=" padding.\n\n.. _`RFC 4648`: https://tools.ietf.org/html/rfc4648\n\nInstalling\n----------\n\n.. code:: bash\n\n   python3 -m pip install unpaddedbase64\n\nUsing\n-----\n\n.. code:: python\n\n    import unpaddedbase64\n    assert (unpaddedbase64.encode_base64(b\'\\x00\')) == \'AA\'\n    assert (unpaddedbase64.decode_base64(\'AA\')) == b\'\\x00\'\n',
    'author': 'The Matrix.org Foundation C.I.C.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matrix-org/python-unpaddedbase64',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
