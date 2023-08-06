from rfq.rfq import Queue


def main(args):
    topic = args.topic
    queue = args.queue

    q = Queue()

    msgids = q.purge(topic=topic, queue=queue)

    for msgid in msgids:
        print(msgid)
