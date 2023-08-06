# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['quart_schema']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8', 'pyhumps>=1.6.1', 'quart>=0.14']

extras_require = \
{':python_version < "3.8"': ['typing_extensions']}

setup_kwargs = {
    'name': 'quart-schema',
    'version': '0.7.0',
    'description': 'A Quart extension to provide schema validation',
    'long_description': 'Quart-Schema\n============\n\n|Build Status| |docs| |pypi| |python| |license|\n\nQuart-Schema is a Quart extension that provides schema validation and\nauto-generated API documentation. This is particularly useful when\nwriting RESTful APIs.\n\nQuickstart\n----------\n\nQuart-Schema can validate an existing Quart route by decorating it\nwith ``validate_querystring``, ``validate_request``, or\n``validate_response``. It can also validate the JSON data sent and\nreceived over websockets using the ``send_as`` and ``receive_as``\nmethods,\n\n.. code-block:: python\n\n    from datetime import datetime\n    from typing import Optional\n\n    from pydantic.dataclasses import dataclass\n    from quart import Quart\n    from quart_schema import QuartSchema, validate_request, validate_response\n\n    app = Quart(__name__)\n    QuartSchema(app)\n\n    @dataclass\n    class Todo:\n        task: str\n        due: Optional[datetime]\n\n    @app.route("/", methods=["POST"])\n    @validate_request(Todo)\n    @validate_response(Todo, 201)\n    async def create_todo(data: Todo) -> Todo:\n        ... # Do something with data, e.g. save to the DB\n        return data, 201\n\n    @app.websocket("/ws")\n    async def ws() -> None:\n        while True:\n            data = await websocket.receive_as(Todo)\n            ... # Do something with data, e.g. save to the DB\n            await websocket.send_as(data, Todo)\n\nThe documentation is served by default at ``/openapi.json`` according\ntot eh OpenAPI standard, or at ``/docs`` for a `SwaggerUI\n<https://swagger.io/tools/swagger-ui/>`_ interface, or ``/redocs`` for\na `redoc <https://github.com/Redocly/redoc>`_ interface. Note that\nthere is currently no documentation standard for WebSockets.\n\nContributing\n------------\n\nQuart-Schema is developed on `GitLab\n<https://gitlab.com/pgjones/quart-schema>`_. If you come across an\nissue, or have a feature request please open an `issue\n<https://gitlab.com/pgjones/quart-schema/issues>`_. If you want to\ncontribute a fix or the feature-implementation please do (typo fixes\nwelcome), by proposing a `merge request\n<https://gitlab.com/pgjones/quart-schema/merge_requests>`_.\n\nTesting\n~~~~~~~\n\nThe best way to test Quart-Schema is with `Tox\n<https://tox.readthedocs.io>`_,\n\n.. code-block:: console\n\n    $ pip install tox\n    $ tox\n\nthis will check the code style and run the tests.\n\nHelp\n----\n\nThe Quart-Schema `documentation\n<https://pgjones.gitlab.io/quart-schema/>`_ is the best places to\nstart, after that try searching `stack overflow\n<https://stackoverflow.com/questions/tagged/quart>`_ or ask for help\n`on gitter <https://gitter.im/python-quart/lobby>`_. If you still\ncan\'t find an answer please `open an issue\n<https://gitlab.com/pgjones/quart-schema/issues>`_.\n\n\n.. |Build Status| image:: https://gitlab.com/pgjones/quart-schema/badges/master/pipeline.svg\n   :target: https://gitlab.com/pgjones/quart-schema/commits/master\n\n.. |docs| image:: https://img.shields.io/badge/docs-passing-brightgreen.svg\n   :target: https://pgjones.gitlab.io/quart-schema/\n\n.. |pypi| image:: https://img.shields.io/pypi/v/quart-schema.svg\n   :target: https://pypi.python.org/pypi/Quart-Schema/\n\n.. |python| image:: https://img.shields.io/pypi/pyversions/quart-schema.svg\n   :target: https://pypi.python.org/pypi/Quart-Schema/\n\n.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg\n   :target: https://gitlab.com/pgjones/quart-schema/blob/master/LICENSE\n',
    'author': 'pgjones',
    'author_email': 'philip.graham.jones@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/pgjones/quart-schema/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
