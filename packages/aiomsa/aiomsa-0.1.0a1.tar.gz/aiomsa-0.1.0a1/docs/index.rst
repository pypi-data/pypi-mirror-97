==================================
Welcome to aiomsa's documentation!
==================================

*aiomsa* is a Python 3.7+ framework built using :mod:`asyncio`. At its core,
*aiomsa* provides a simple and standardized way to write xApps that can be deployed as
microservices in Python.

In addition, *aiomsa* creates an HTTP server with
:doc:`preinstalled endpoints<./routes>` for xApp configuration and Prometheus metric
exposition among others. Developers can add their own endpoints to this server for their
own application logic.

Usage
=====

The entrypoint for the *aiomsa* framework is the :func:`~.init` function.

.. autofunction:: aiomsa.init

.. _aiomsa-quickstart:

Quickstart
----------

The follwing example shows how to use *aiomsa* to create a simple microservice for
consuming and printing records from an E2T subscription.

A ``lambda`` wrapper of ``async_main``, the entrypoint for the service's business logic,
and its parameters are supplied to the :func:`~.init` function.

.. code-block:: python

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

Installation
============

*aiomsa* can be installed from PyPI.

.. code-block:: bash

    $ pip install aiomsa

You can also get the latest code from GitHub.

.. code-block:: bash

    $ poetry add git+https://github.com/facebookexternal/aiomsa

Dependencies
============

* Python 3.7+
* aiohttp
* aiohttp-swagger
* betterproto

Table of Contents
=================

.. toctree::
   :name: mastertoc
   :maxdepth: 2

   reference
   misc
