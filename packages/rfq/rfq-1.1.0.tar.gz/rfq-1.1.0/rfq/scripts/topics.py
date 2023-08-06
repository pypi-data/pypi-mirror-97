from rfq.rfq import Queue


def main(args):
    q = Queue()

    for topic in q.topics():
        print(topic)
