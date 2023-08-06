# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rfq', 'rfq.scripts']

package_data = \
{'': ['*']}

install_requires = \
['redis>=3.5.3,<4.0.0']

extras_require = \
{'hiredis': ['hiredis>=1.1.0,<2.0.0']}

entry_points = \
{'console_scripts': ['rfq = rfq.scripts.__main__:main']}

setup_kwargs = {
    'name': 'rfq',
    'version': '1.1.0',
    'description': 'Simple language-agnostic message queues: tools, conventions, examples',
    'long_description': '<h1 align=\'center\'>rfq</h1>\n\n<p align=center>\n  Simple language-agnostic message queues: tools, conventions, examples\n  <img src="assets/rfq.png" />\n</p>\n\n## Table of Contents\n\n1. [Overview](#overview)\n2. [Features](#features)\n3. [Installation](#installation)\n4. [Usage](#usage)\n5. [Example](#example)\n6. [Development](#development)\n7. [License](#license)\n\n\n## Overview\n\nImplementing a reliable message queue with redis is possible but has to follow certain [best practices](https://redis.io/commands/rpoplpush#pattern-reliable-queue).\nThe goal of this project is to provide a simple reliable message queue Python library and command line wrapper while following best practices and capturing conventions as code.\n\nThe [underlying queue design](./design.md) makes it simple to write adapters for other languages, e.g. see [rfq.js](https://github.com/robofarmio/rfq.js) for a Javascript/Typescript integration.\n\nContext: we\'ve started this project because we needed a simple queue abstraction easily accessible through different languages and abstract away over manually using redis.\nThis project started back when we were running on a single dedicated server, but we are still using it for both local development as well as production.\n\n\n## Features\n\n- Library and command line wrappers capturing best practices\n- Throughput: https://redis.io/topics/benchmarks\n- Persistence: https://redis.io/topics/persistence\n- Exactly-Once Processing: Messages are delivered once, and stay in the system until clients commit them\n- First-In-First-Out: The order in which messages are sent and received is strictly preserved\n- Payload size: Up to a maximum of 512 MB in message size\n- Total messages: Up to a total of 2^32-1 messages in the system\n\n\n## Installation\n\nWe publish `rfq` to PyPI at https://pypi.org/project/rfq/\n\nInstall with `poetry`\n\n    poetry add rfq\n\nInstall with `pip`\n\n    pip install rfq\n\n\n## Usage\n\nThe command line tool and library can be configured by setting the environment variables\n\n    export RFQ_REDIS_HOST=localhost\n    export RFQ_REDIS_PORT=6397\n\nThe library allows you to provide a custom redis instance.\n\nFor the command line wrapper, see\n\n    $ rfq --help\n\nThe command line tool comes with bash completions; install them via\n\n    rfq completions bash > /etc/bash_completion.d/rfq.bash-completion\n\nFor the Python library see the `Queue` and `Task` class in [`rfq/rfq.py`](./rfq/rfq.py).\n\nUnderstand\n- There is a "backlog" for published messages not yet consumed\n- There is a "nextlog" for published messages consumed but not yet committed\n- In case commit never happens (e.g. crashes), "harvest" moves messages from "nextlog" back into "backlog"\n\n\n## Example\n\n```python\nfrom rfq.rfq import Queue\n\n# The default queue connects to redis at localhost:6397\n# you can pass a custom redis instance or use env vars\n# to configure the redis host and port the queue uses\nqueue = Queue()\n\n# Publishing a message of key-value pairs to a topic\nqueue.publish("mytopic", {"k": "v"})\n\n# Consuming from a topic returns a task; you must\n# only commit the task with .done() once you\'ve\n# successfully completed working on it\ntask = queue.consume("mytopic")\nprint(task.result())\ntask.done()\n```\n\n\n## Development\n\nFor development\n\n    make\n\n    make run\n    $ rfq --help\n\n    $ exit\n    make down\n\nInside the self-contained reproducible container\n\n    flake8 rfq\n    mypy rfq\n    pytest\n\n## License\n\nCopyright © 2020 robofarm\n\nDistributed under the MIT License (MIT).\n',
    'author': 'Robofarm',
    'author_email': 'hello@robofarm.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
