#!/usr/bin/env python
import paramiko
import sys
import os
import re


def uptime(i, queue):

    while True:
        host = queue.get()
        client = paramiko.SSHClient()
        client.get_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=22)
        stdin, stdout, stderr = client.exec_command('uptime')
        result = stdout.read()
        client.close()
        res_dict = re.match(r'.*up\s+(?P<uptime>.*?),\s+([0-9]+) users?', result.strip()).groupdict()
        print host, res_dict['uptime']
        queue.task_done()


def produce_hosts(file_name, queue):
    """ Produces work for the uptime worker.
    """

    with open(file_name) as fh:
        for line in fh:
            queue.put(line.strip())


if __name__ == '__main__':
    from multiprocessing import Process, JoinableQueue

    if len(sys.argv) < 3:
        sys.exit('Usage: %s filename concurrency' % sys.argv[0])

    file_name = sys.argv[1]
    concurrency = int(sys.argv[2])

    if not os.path.exists(file_name):
        sys.exit('ERROR: data file %s was not found!' % sys.argv[1])

    queue = JoinableQueue(concurrency)
    ssh_workers = [Process(target=uptime, args=(i, queue)) for i in xrange(concurrency)]

    for sshw in ssh_workers:
        sshw.daemon = True
        sshw.start()

    produce_hosts(file_name, queue)
    queue.join()
