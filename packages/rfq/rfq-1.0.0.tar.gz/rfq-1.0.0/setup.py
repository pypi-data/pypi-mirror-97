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
    'version': '1.0.0',
    'description': 'Simple language-agnostic message queues: tools, conventions, examples',
    'long_description': '<h1 align=\'center\'>rfq</h1>\n\n<p align=center>\n  Simple language-agnostic message queues: tools, conventions, examples\n  <img src="assets/rfq.png" />\n</p>\n\n## Table of Contents\n\n1. [Overview](#overview)\n1. [Features](#features)\n2. [Usage](#usage)\n    - [info](#info)\n    - [list-topics](#list-topics)\n    - [list-queue](#list-queue)\n    - [purge-queue](#purge-queue)\n    - [publish](#publish)\n    - [consume](#consume)\n    - [harvest](#harvest)\n3. [Development](#development)\n4. [License](#license)\n\n\n## Overview\n\nImplementing a reliable message queue with redis is possible but has to follow certain [best practices](https://redis.io/commands/rpoplpush#pattern-reliable-queue).\nThe goal of this project is to provide a simple reliable message queue Python library and command line wrappers while following best practices and capturing conventions as code.\nSee [rfq.js](https://github.com/robofarmio/rfq.js) for a simple Javascript/Typescript integration.\n\n\n## Features\n\n- Library and command line wrappers capturing best practices\n- Throughput: https://redis.io/topics/benchmarks\n- Persistence: https://redis.io/topics/persistence\n- Exactly-Once Processing: Messages are delivered once, and stay in the system until clients consume them\n- First-In-First-Out: The order in which messages are sent and received is strictly preserved\n- Payload size: Up to a maximum of 512 MB in message size\n- Total messages: Up to a total of 2^32-1 messages in the system\n\n\n## Usage\n\nThe following describes rfq in terms of command line wrappers; [design.md](./design.md) describes the low level design.\n\nThe command line tool and library can be configured by setting the environment variables\n\n    export RFQ_REDIS_HOST=localhost\n    export RFQ_REDIS_PORT=6397\n\nfor the default redis host and port when not providing a custom redis instance.\n\n\n### info\n\nShows information for all topics and queues. We recommend running it in an interval with `watch`\n\n    watch rfq info\n\n    topic      mytopic\n    backlog    10      #######################\n    nextlog    2       #######\n\n\n### list-topics\n\nList all active topics\n\n    rfq list-topics\n    ndvi\n\n\n### list-queue\n\nList messages in the backlog (work not yet started)\n\n    rfq list-queue --topic \'ndvi\'\n    eeba0c1642ab11eaa480a4c3f0958f5d\n    ede1296442ab11eabdb9a4c3f0958f5d\n\nList messages in the nextlog (work started but not yet committed)\n\n    rfq list-queue--topic \'ndvi\' --queue nextlog\n    eeba0c1642ab11eaa480a4c3f0958f5d\n\n\n### purge-queue\n\nDeletes messages in a queue\n\n    rfq purge-queue --topic \'ndvi\'\n    eeba0c1642ab11eaa480a4c3f0958f5d\n    ede1296442ab11eabdb9a4c3f0958f5d\n\n\n### publish\n\nPublish messages to a topic\n\n    rfq publish --topic \'ndvi\' --message \'{ "tile": "T32UNE" }\'\n    eeba0c1642ab11eaa480a4c3f0958f5d\n    rfq publish --topic \'ndvi\' --message \'{ "tile": "T33UVU" }\'\n    ede1296442ab11eabdb9a4c3f0958f5d\n\nNote: messages and are a flat map of key-value pairs, see [issue/1](https://github.com/robofarmio/rfq/issues/1)\n\n\n### consume\n\nConsume a message, working on it (dummy sleep), then commit the message when done\n\n    rfq consume --topic \'ndvi\'\n    { "tile": "T32UNE" }\n\n\n### harvest\n\nHarvest messages from the nextlog back into the backlog\n\n    rfq harvest --topic \'ndvi\'\n    eeba0c1642ab11eaa480a4c3f0958f5d\n\nNote: messages end up in the nextlog when workers start processing but haven\'t committed them yet.\n\n\n## Development\n\nFor development\n\n    make\n\n    make run\n    $ rfq --help\n\n    $ exit\n    make down\n\nOr run the commands directly from the docker container with\n\n    docker run -e RFQ_REDIS_HOST=MyRedisHost robofarm/rfq --help\n\n\n## License\n\nCopyright © 2020 robofarm\n\nDistributed under the MIT License (MIT).\n',
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
