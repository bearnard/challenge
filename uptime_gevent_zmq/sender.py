#!/usr/bin/env python
import gevent
from gevent_zeromq import zmq
import sys
import os
import time


def serve(sender, file_name):
    """ sends ssh hosts to workers.
    """
    with open(file_name) as fh:
        for line in fh:
            sender.send(line.strip())


if __name__ == '__main__':

    if len(sys.argv) < 3:
        sys.exit('Usage: %s filename watermark_limit' % sys.argv[0])

    file_name = sys.argv[1]
    if not os.path.exists(file_name):
        sys.exit('ERROR: data file %s was not found!' % sys.argv[1])

    watermark = int(sys.argv[2])
    # server
    context = zmq.Context()

    # Socket to send messages on
    sender = context.socket(zmq.PUSH)

    # Optional HighWatermark to block if workers are busy
    sender.setsockopt(zmq.SNDHWM, watermark)
    sender.bind("tcp://*:5557")

    # Socket with direct access to the uptime results sink.
    sink = context.socket(zmq.PUSH)
    sink.connect("tcp://localhost:5558")


    sink.send('file: %s' % file_name)

    print "Sending ssh hosts to workers..."
    server = gevent.spawn(serve, sender, file_name)
    server.join()

