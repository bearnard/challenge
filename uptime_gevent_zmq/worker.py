#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from gevent.queue import JoinableQueue
from gevent_zeromq import zmq
import gevent
import paramiko
import sys
import os
import re
import signal

def uptime(i, worker_id, queue, sender):
    client = paramiko.SSHClient()
    #  prevent blocking while loading host keys
    client.get_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    while True:
        try:
            host = queue.get(block=True)
            client.connect(host, port=22)
            stdin, stdout, stderr = client.exec_command('uptime')
            result = stdout.read()
            client.close()
            res_dict = re.match(r'.*up\s+(?P<uptime>.*?),\s+([0-9]+) users?', result.strip()).groupdict()
            sender.send("worker_id: %s_%s, host: %s, result: %s" % (worker_id, i, host, res_dict['uptime']))
        except Exception, e:
            sender.send("worker_id: %s_%s, host: %s, error: %s" % (worker_id, i, host, str(e)))
        finally:
            queue.task_done()


def recv_hosts(receiver, queue):
    """ Receives hosts for the uptime worker.
    """
    while True:
        message = receiver.recv()
        print "Recieved Host:", message
        queue.put(message.strip(), block=True)



def watchdog(delay=0.2, threshold = 0.2): # 0.2 sec. check interval, 20% threshold
    def signalhandler(sig, frame):
        print "Blocking Code detected"
        print gevent.greenlet.getcurrent()
    signal.signal(signal.SIGALRM, signalhandler)
    while True:
        signal.setitimer(signal.ITIMER_REAL,delay + delay * threshold)
        gevent.sleep(delay)


if __name__ == '__main__':

    if len(sys.argv) < 3:
        sys.exit('Usage: %s worker_id concurrency' % sys.argv[0])

    wd = gevent.spawn(watchdog)
    worker_id = sys.argv[1]
    concurrency = int(sys.argv[2])
    queue = JoinableQueue(maxsize=concurrency)
    pool = Pool(concurrency)

    context = zmq.Context()
    # Socket to receive ssh hosts on
    receiver = context.socket(zmq.PULL)
    #receiver.setsockopt(zmq.RCVHWM, concurrency)
    receiver.connect("tcp://localhost:5557")

    # Socket to send uptime results to
    sender = context.socket(zmq.PUSH)
    sender.connect("tcp://localhost:5558")

    ssh_workers = [
        pool.spawn(uptime, i, worker_id, queue, sender) for i in xrange(concurrency)
    ]
    recv_hosts(receiver, queue)
    queue.join()
