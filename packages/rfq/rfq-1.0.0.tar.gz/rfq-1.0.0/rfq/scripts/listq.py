from rfq.rfq import Queue


def main(args):
    topic = args.topic
    queue = args.queue

    q = Queue()

    for msgid in q.listq(topic=topic, queue=queue):
        print(msgid)
