import json

from rfq.rfq import Queue


def main(args):
    topic = args.topic
    message = json.loads(args.message)
    front = args.front

    q = Queue()

    msgid = q.publish(topic=topic, message=message, front=front)

    print(msgid)
