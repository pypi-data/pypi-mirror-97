<h1 align='center'>rfq</h1>

<p align=center>
  Simple language-agnostic message queues: tools, conventions, examples
  <img src="assets/rfq.png" />
</p>

## Table of Contents

1. [Overview](#overview)
1. [Features](#features)
2. [Usage](#usage)
    - [info](#info)
    - [list-topics](#list-topics)
    - [list-queue](#list-queue)
    - [purge-queue](#purge-queue)
    - [publish](#publish)
    - [consume](#consume)
    - [harvest](#harvest)
3. [Development](#development)
4. [License](#license)


## Overview

Implementing a reliable message queue with redis is possible but has to follow certain [best practices](https://redis.io/commands/rpoplpush#pattern-reliable-queue).
The goal of this project is to provide a simple reliable message queue Python library and command line wrappers while following best practices and capturing conventions as code.
See [rfq.js](https://github.com/robofarmio/rfq.js) for a simple Javascript/Typescript integration.


## Features

- Library and command line wrappers capturing best practices
- Throughput: https://redis.io/topics/benchmarks
- Persistence: https://redis.io/topics/persistence
- Exactly-Once Processing: Messages are delivered once, and stay in the system until clients consume them
- First-In-First-Out: The order in which messages are sent and received is strictly preserved
- Payload size: Up to a maximum of 512 MB in message size
- Total messages: Up to a total of 2^32-1 messages in the system


## Usage

The following describes rfq in terms of command line wrappers; [design.md](./design.md) describes the low level design.

The command line tool and library can be configured by setting the environment variables

    export RFQ_REDIS_HOST=localhost
    export RFQ_REDIS_PORT=6397

for the default redis host and port when not providing a custom redis instance.


### info

Shows information for all topics and queues. We recommend running it in an interval with `watch`

    watch rfq info

    topic      mytopic
    backlog    10      #######################
    nextlog    2       #######


### list-topics

List all active topics

    rfq list-topics
    ndvi


### list-queue

List messages in the backlog (work not yet started)

    rfq list-queue --topic 'ndvi'
    eeba0c1642ab11eaa480a4c3f0958f5d
    ede1296442ab11eabdb9a4c3f0958f5d

List messages in the nextlog (work started but not yet committed)

    rfq list-queue--topic 'ndvi' --queue nextlog
    eeba0c1642ab11eaa480a4c3f0958f5d


### purge-queue

Deletes messages in a queue

    rfq purge-queue --topic 'ndvi'
    eeba0c1642ab11eaa480a4c3f0958f5d
    ede1296442ab11eabdb9a4c3f0958f5d


### publish

Publish messages to a topic

    rfq publish --topic 'ndvi' --message '{ "tile": "T32UNE" }'
    eeba0c1642ab11eaa480a4c3f0958f5d
    rfq publish --topic 'ndvi' --message '{ "tile": "T33UVU" }'
    ede1296442ab11eabdb9a4c3f0958f5d

Note: messages and are a flat map of key-value pairs, see [issue/1](https://github.com/robofarmio/rfq/issues/1)


### consume

Consume a message, working on it (dummy sleep), then commit the message when done

    rfq consume --topic 'ndvi'
    { "tile": "T32UNE" }


### harvest

Harvest messages from the nextlog back into the backlog

    rfq harvest --topic 'ndvi'
    eeba0c1642ab11eaa480a4c3f0958f5d

Note: messages end up in the nextlog when workers start processing but haven't committed them yet.


## Development

For development

    make

    make run
    $ rfq --help

    $ exit
    make down

Or run the commands directly from the docker container with

    docker run -e RFQ_REDIS_HOST=MyRedisHost robofarm/rfq --help


## License

Copyright © 2020 robofarm

Distributed under the MIT License (MIT).
