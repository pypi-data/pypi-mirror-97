import math

from rfq.rfq import Queue


def main(args):
    q = Queue()

    n, m = q.version()

    print("rfq {}".format(n))
    print("redis {}".format(m))
