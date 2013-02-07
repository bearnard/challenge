#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from gevent.queue import JoinableQueue
import paramiko
import sys
import os
import re

def uptime(i, queue):
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
            print host, res_dict['uptime']
        except:
            print "Failed:", host
        finally:
            queue.task_done()


def produce_hosts(file_name, queue):
    """ Produces work for the uptime worker.
    """

    with open(file_name) as fh:
        for line in fh:
            queue.put(line.strip(), block=True)


if __name__ == '__main__':

    if len(sys.argv) < 3:
        sys.exit('Usage: %s filename concurrency' % sys.argv[0])

    file_name = sys.argv[1]
    concurrency = int(sys.argv[2])
    if not os.path.exists(file_name):
        sys.exit('ERROR: data file %s was not found!' % sys.argv[1])

    queue = JoinableQueue(maxsize=concurrency)
    pool = Pool(concurrency)

    ssh_workers = [
        pool.spawn(uptime, i, queue) for i in xrange(concurrency)
    ]
    produce_hosts(file_name, queue)
    queue.join()
