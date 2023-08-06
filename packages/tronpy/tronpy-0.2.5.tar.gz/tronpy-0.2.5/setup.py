# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tronpy', 'tronpy.keys', 'tronpy.providers']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.0.0,<3.0.0',
 'ecdsa>=0.15,<0.16',
 'eth_abi>=2.1.1,<3.0.0',
 'httpx>=0.16.1,<0.17.0',
 'pycryptodome>=3.9.7,<4.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'tronpy',
    'version': '0.2.5',
    'description': 'TRON Python client library',
    'long_description': '# tronpy\n\n[![PyPI version](https://badge.fury.io/py/tronpy.svg)](https://pypi.org/project/tronpy/)\n\nTRON Python Client Library. [Documentation](https://tronpy.readthedocs.io/en/latest/index.html)\n\n## How to use\n\n```python\nfrom tronpy import Tron\n\nclient = Tron(network=\'nile\')\n# Private key of TJzXt1sZautjqXnpjQT4xSCBHNSYgBkDr3\npriv_key = PrivateKey(bytes.fromhex("8888888888888888888888888888888888888888888888888888888888888888"))\n\ntxn = (\n    client.trx.transfer("TJzXt1sZautjqXnpjQT4xSCBHNSYgBkDr3", "TVjsyZ7fYF3qLF6BQgPmTEZy1xrNNyVAAA", 1_000)\n    .memo("test memo")\n    .build()\n    .inspect()\n    .sign(priv_key)\n    .broadcast()\n)\n\nprint(txn)\n# > {\'result\': True, \'txid\': \'5182b96bc0d74f416d6ba8e22380e5920d8627f8fb5ef5a6a11d4df030459132\'}\nprint(txn.wait())\n# > {\'id\': \'5182b96bc0d74f416d6ba8e22380e5920d8627f8fb5ef5a6a11d4df030459132\', \'blockNumber\': 6415370, \'blockTimeStamp\': 1591951155000, \'contractResult\': [\'\'], \'receipt\': {\'net_usage\': 283}}\n```\n\n### Async Client\n\n```python\nimport asyncio\n\nfrom tronpy import AsyncTron\nfrom tronpy.keys import PrivateKey\n\n# private key of TMisHYBVvFHwKXHPYTqo8DhrRPTbWeAM6z\npriv_key = PrivateKey(bytes.fromhex("8888888888888888888888888888888888888888888888888888888888888888"))\n\nasync def transfer():\n    async with AsyncTron(network=\'nile\') as client:\n        print(client)\n\n        txb = (\n            client.trx.transfer("TJzXt1sZautjqXnpjQT4xSCBHNSYgBkDr3", "TVjsyZ7fYF3qLF6BQgPmTEZy1xrNNyVAAA", 1_000)\n            .memo("test memo")\n            .fee_limit(100_000_000)\n        )\n        txn = await txb.build()\n        print(txn)\n        txn_ret = await txn.sign(priv_key).broadcast()\n        print(txn_ret)\n        # > {\'result\': True, \'txid\': \'edc2a625752b9c71fdd0d68117802860c6adb1a45c19fd631a41757fa334d72b\'}\n        print(await txn_ret.wait())\n        # > {\'id\': \'edc2a625752b9c71fdd0d68117802860c6adb1a45c19fd631a41757fa334d72b\', \'blockNumber\': 10163821, \'blockTimeStamp\': 1603368072000, \'contractResult\': [\'\'], \'receipt\': {\'net_usage\': 283}}\n\nif __name__ == \'__main__\':\n    asyncio.run(transfer())\n```\n\nOr close async client manually:\n\n```python\nfrom httpx import AsyncClient, Timeout\nfrom tronpy.providers.async_http import AsyncHTTPProvider\nfrom tronpy.defaults import CONF_NILE\n\n\nasync def transfer():\n    _http_client = AsyncClient(limits=Limits(max_connections=100, max_keepalive_connections=20),\n                               timeout=Timeout(timeout=10, connect=5, read=5))\n    provider = AsyncHTTPProvider(CONF_NILE, client=_http_client)\n    client = AsyncTron(provider=provider)\n    print(client)\n\n    priv_key = PrivateKey(bytes.fromhex("8888888888888888888888888888888888888888888888888888888888888888"))\n    txb = (\n        client.trx.transfer("TJzXt1sZautjqXnpjQT4xSCBHNSYgBkDr3", "TVjsyZ7fYF3qLF6BQgPmTEZy1xrNNyVAAA", 1_000)\n        .memo("test memo")\n        .fee_limit(100_000_000)\n    )\n    txn = await txb.build()\n    print(txn)\n    txn_ret = await txn.sign(priv_key).broadcast()\n\n    print(txn_ret)\n    print(await txn_ret.wait())\n    await client.close()\n\nif __name__ == \'__main__\':\n    asyncio.run(transfer())\n```\n',
    'author': 'andelf',
    'author_email': 'andelf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andelf/tronpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
