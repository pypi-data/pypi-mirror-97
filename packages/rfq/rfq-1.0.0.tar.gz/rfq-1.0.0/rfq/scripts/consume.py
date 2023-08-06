import time

from rfq.rfq import Queue


def main(args):
    topic = args.topic

    q = Queue()

    task = q.consume(topic=topic)

    work(task.result())

    task.done()


def work(payload):
    print(payload)
    time.sleep(1)
