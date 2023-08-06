# aiomsa
[![build](https://github.com/facebookexternal/aiomsa/workflows/build/badge.svg)](https://github.com/facebookexternal/aiomsa/actions?query=workflow%3Abuild)
[![style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*aiomsa* is a Python 3.7+ framework built using `asyncio`. At its core, *aiomsa*
provides a simple and standardized way to write xApps that can be deployed as
microservices in Python.

## Installation
*aiomsa* can be installed from PyPI.
```bash
pip install aiomsa
```

You can also get the latest code from GitHub.
```bash
poetry add git+https://github.com/facebookexternal/aiomsa
```

## Getting Started
The follwing example shows how to use *aiomsa* to create a simple xApp for subscribing
to the E2T service for a particular custom service model.

```python
import asyncio
import json

from aiomsa import init
from aiomsa.e2 import E2

from .models import MyModel


async def consume(queue):
   while True:
      record = await queue.get()
      print(record)

async def produce(queue):
   conns = await E2.list_nodes()
   subscription_id = await E2.subscribe(
      conns[0],
      service_model_id="mymodel_v1",
      trigger=bytes(MyModel(param="foo")),
      queue=queue,
   )

async def async_main():
   """Create an asyncio.Queue to pub/sub records."""

   queue = asyncio.Queue()
   await asyncio.gather(produce(queue), consume(queue))


if __name__ == "__main__":
   with open("./config.json") as f:
      config = json.load(f)

   E2.configure(**config)
   init(lambda: async_main())
```
