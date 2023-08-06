import math

from rfq.rfq import Queue


def main(args):
    q = Queue()

    for topic in sorted(q.topics()):
        backlog, nextlog = q.info(topic=topic)

        # Show a rough visual representation of the queue's sizes.
        # We do not know the order of magnitude of messages our
        # users are working with, so we map the sizes to roughly
        # [0, 140] '#' characters for [0, 1.000.000] messages.

        n = int(10 * math.log(backlog + 1))
        m = int(10 * math.log(nextlog + 1))

        print("topic\t\t{}".format(topic))
        print("backlog\t\t{}\t\t{}".format(backlog, n * "#"))
        print("nextlog\t\t{}\t\t{}".format(nextlog, m * "#"))
        print()
