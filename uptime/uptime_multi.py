#!/usr/bin/env python
from multiprocessing import Pool
import warnings
import paramiko
import sys
import os
import re


def uptime(host):
    client = paramiko.SSHClient()
    client.get_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=24)
    stdin, stdout, stderr = client.exec_command('uptime')
    result = stdout.read()
    client.close()
    return host, result


def chunk_lines(file_name, chunk_size):
    """ Yields lines from the hosts file, useful
        when dealing with really large files.
    """

    with open(file_name) as fh:
        count = 0
        lines = []
        for line in fh:
            lines.append(line.strip())
            count += 1
            if count == chunk_size:
                tmp_lines = lines
                lines = []
                count = 0
                yield tmp_lines
        yield lines


if __name__ == '__main__':

    if len(sys.argv) < 3:
        sys.exit('Usage: %s filename concurrency' % sys.argv[0])

    file_name = sys.argv[1]
    concurrency = int(sys.argv[2])

    if not os.path.exists(file_name):
        sys.exit('ERROR: data file %s was not found!' % sys.argv[1])

    hosts = []
    for hosts in chunk_lines(file_name, concurrency):

        pool = Pool(processes=concurrency)

        for host, result in pool.imap(uptime, hosts):
            res_dict = re.match(r'.*up\s+(?P<uptime>.*?),\s+([0-9]+) users?', result.strip()).groupdict()
            print "Host: %s" % host, res_dict['uptime']

