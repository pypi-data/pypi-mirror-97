<h1 align='center'>rfq</h1>

<p align=center>
  Simple language-agnostic message queues: tools, conventions, examples
  <img src="assets/rfq.png" />
</p>

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Example](#example)
6. [Development](#development)
7. [License](#license)


## Overview

Implementing a reliable message queue with redis is possible but has to follow certain [best practices](https://redis.io/commands/rpoplpush#pattern-reliable-queue).
The goal of this project is to provide a simple reliable message queue Python library and command line wrapper while following best practices and capturing conventions as code.

The [underlying queue design](./design.md) makes it simple to write adapters for other languages, e.g. see [rfq.js](https://github.com/robofarmio/rfq.js) for a Javascript/Typescript integration.

Context: we've started this project because we needed a simple queue abstraction easily accessible through different languages and abstract away over manually using redis.
This project started back when we were running on a single dedicated server, but we are still using it for both local development as well as production.


## Features

- Library and command line wrappers capturing best practices
- Throughput: https://redis.io/topics/benchmarks
- Persistence: https://redis.io/topics/persistence
- Exactly-Once Processing: Messages are delivered once, and stay in the system until clients commit them
- First-In-First-Out: The order in which messages are sent and received is strictly preserved
- Payload size: Up to a maximum of 512 MB in message size
- Total messages: Up to a total of 2^32-1 messages in the system


## Installation

We publish `rfq` to PyPI at https://pypi.org/project/rfq/

Install with `poetry`

    poetry add rfq

Install with `pip`

    pip install rfq


## Usage

The command line tool and library can be configured by setting the environment variables

    export RFQ_REDIS_HOST=localhost
    export RFQ_REDIS_PORT=6397

The library allows you to provide a custom redis instance.

For the command line wrapper, see

    $ rfq --help

The command line tool comes with bash completions; install them via

    rfq completions bash > /etc/bash_completion.d/rfq.bash-completion

For the Python library see the `Queue` and `Task` class in [`rfq/rfq.py`](./rfq/rfq.py).

Understand
- There is a "backlog" for published messages not yet consumed
- There is a "nextlog" for published messages consumed but not yet committed
- In case commit never happens (e.g. crashes), "harvest" moves messages from "nextlog" back into "backlog"


## Example

```python
from rfq.rfq import Queue

# The default queue connects to redis at localhost:6397
# you can pass a custom redis instance or use env vars
# to configure the redis host and port the queue uses
queue = Queue()

# Publishing a message of key-value pairs to a topic
queue.publish("mytopic", {"k": "v"})

# Consuming from a topic returns a task; you must
# only commit the task with .done() once you've
# successfully completed working on it
task = queue.consume("mytopic")
print(task.result())
task.done()
```


## Development

For development

    make

    make run
    $ rfq --help

    $ exit
    make down

Inside the self-contained reproducible container

    flake8 rfq
    mypy rfq
    pytest

## License

Copyright © 2020 robofarm

Distributed under the MIT License (MIT).
