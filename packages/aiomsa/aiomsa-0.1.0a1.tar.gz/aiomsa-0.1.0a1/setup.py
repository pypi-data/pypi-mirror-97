# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiomsa',
 'aiomsa.onos_api',
 'aiomsa.onos_api.gnmi',
 'aiomsa.onos_api.gnmi_ext',
 'aiomsa.onos_api.gogoproto',
 'aiomsa.onos_api.onos',
 'aiomsa.onos_api.onos.config',
 'aiomsa.onos_api.onos.config.admin',
 'aiomsa.onos_api.onos.config.change',
 'aiomsa.onos_api.onos.config.change.device',
 'aiomsa.onos_api.onos.config.change.network',
 'aiomsa.onos_api.onos.config.diags',
 'aiomsa.onos_api.onos.config.snapshot',
 'aiomsa.onos_api.onos.config.snapshot.device',
 'aiomsa.onos_api.onos.config.snapshot.network',
 'aiomsa.onos_api.onos.configmodel',
 'aiomsa.onos_api.onos.e2sub',
 'aiomsa.onos_api.onos.e2sub.endpoint',
 'aiomsa.onos_api.onos.e2sub.subscription',
 'aiomsa.onos_api.onos.e2sub.task',
 'aiomsa.onos_api.onos.e2t',
 'aiomsa.onos_api.onos.e2t.admin',
 'aiomsa.onos_api.onos.e2t.e2',
 'aiomsa.onos_api.onos.kpimon',
 'aiomsa.onos_api.onos.ransim',
 'aiomsa.onos_api.onos.ransim.metrics',
 'aiomsa.onos_api.onos.ransim.model',
 'aiomsa.onos_api.onos.ransim.trafficsim',
 'aiomsa.onos_api.onos.ransim.types',
 'aiomsa.onos_api.onos.topo',
 'aiomsa.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-swagger>=1.0.9,<2.0.0',
 'aiohttp>=3.5.4,<4.0.0',
 'betterproto>=2.0.0b2,<3.0.0']

extras_require = \
{'docs': ['furo>=2021.2.21-beta.25,<2022.0.0',
          'sphinx>=3.4.3,<4.0.0',
          'sphinx-autodoc-typehints>=1.11.1,<2.0.0',
          'sphinxcontrib-openapi>=0.7.0,<0.8.0'],
 'prometheus': ['prometheus_async>=19.2.0,<20.0.0'],
 'speedups': ['uvloop>=0.14.0,<0.15.0']}

setup_kwargs = {
    'name': 'aiomsa',
    'version': '0.1.0a1',
    'description': 'Asynchronous xApp framework',
    'long_description': '# aiomsa\n[![build](https://github.com/facebookexternal/aiomsa/workflows/build/badge.svg)](https://github.com/facebookexternal/aiomsa/actions?query=workflow%3Abuild)\n[![style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n*aiomsa* is a Python 3.7+ framework built using `asyncio`. At its core, *aiomsa*\nprovides a simple and standardized way to write xApps that can be deployed as\nmicroservices in Python.\n\n## Installation\n*aiomsa* can be installed from PyPI.\n```bash\npip install aiomsa\n```\n\nYou can also get the latest code from GitHub.\n```bash\npoetry add git+https://github.com/facebookexternal/aiomsa\n```\n\n## Getting Started\nThe follwing example shows how to use *aiomsa* to create a simple xApp for subscribing\nto the E2T service for a particular custom service model.\n\n```python\nimport asyncio\nimport json\n\nfrom aiomsa import init\nfrom aiomsa.e2 import E2\n\nfrom .models import MyModel\n\n\nasync def consume(queue):\n   while True:\n      record = await queue.get()\n      print(record)\n\nasync def produce(queue):\n   conns = await E2.list_nodes()\n   subscription_id = await E2.subscribe(\n      conns[0],\n      service_model_id="mymodel_v1",\n      trigger=bytes(MyModel(param="foo")),\n      queue=queue,\n   )\n\nasync def async_main():\n   """Create an asyncio.Queue to pub/sub records."""\n\n   queue = asyncio.Queue()\n   await asyncio.gather(produce(queue), consume(queue))\n\n\nif __name__ == "__main__":\n   with open("./config.json") as f:\n      config = json.load(f)\n\n   E2.configure(**config)\n   init(lambda: async_main())\n```\n',
    'author': 'Facebook Connectivity',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/facebookexternal/aiomsa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
