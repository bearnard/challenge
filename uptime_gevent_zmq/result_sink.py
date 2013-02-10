#!/usr/bin/env python
from gevent_zeromq import zmq
import sys

if len(sys.argv) < 2:
    sys.exit('Usage: %s filename' % sys.argv[0])

results_file = sys.argv[1]

context = zmq.Context()

# Socket to receive uptime results on
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

s = receiver.recv()

with open(results_file, 'w') as fh:

    while True:
        s = receiver.recv()
        if s.strip() == 'STOP':
            print "STOP Recieved"
            break
        print s
        fh.write('%s\n' % s)
