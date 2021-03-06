#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import paramiko
import sys
import os


def uptime(host):
    client = paramiko.SSHClient()
    client.get_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=22)
    stdin, stdout, stderr = client.exec_command('uptime')
    result = stdout.read()
    client.close()
    return host, result


if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit('Usage: %s filename' % sys.argv[0])

    file_name = sys.argv[1]
    if not os.path.exists(file_name):
        sys.exit('ERROR: data file %s was not found!' % sys.argv[1])

    pool = Pool(25)
    hosts = []

    with open(file_name) as fh:
        for line in fh:
            hosts.append(line.strip())

    for host, result in pool.imap(uptime, hosts):
        print "Host: %s" % host, "Response: ", result

