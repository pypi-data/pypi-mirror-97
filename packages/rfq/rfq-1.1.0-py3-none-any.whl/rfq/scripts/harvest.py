from rfq.rfq import Queue


def main(args):
    topic = args.topic

    q = Queue()

    msgids = q.harvest(topic=topic)

    for msgid in msgids:
        print(msgid)
