from rfq.rfq import Queue


def main(args):
    topic = args.topic

    q = Queue()

    try:
        task = q.consume(topic=topic)

        work(task.result())

        task.done()
    except KeyboardInterrupt:
        pass


def work(payload):
    print(payload)
