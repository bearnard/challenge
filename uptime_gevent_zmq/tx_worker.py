#!/usr/bin/env python
import sys
import os
import re
from zope.interface import implements

from optparse import OptionParser
from twisted.python.failure import Failure
from twisted.python.log import err
from twisted.internet.error import ConnectionDone
from twisted.internet.defer import Deferred, succeed
from twisted.internet.interfaces import IStreamClientEndpoint
from twisted.internet.protocol import Factory, Protocol

from twisted.conch.ssh.common import NS
from twisted.conch.ssh.channel import SSHChannel
from twisted.conch.ssh.transport import SSHClientTransport
from twisted.conch.ssh.connection import SSHConnection
from twisted.conch.client.default import SSHUserAuthClient
from twisted.conch.client.options import ConchOptions
from txzmq import ZmqEndpoint, ZmqFactory, ZmqPushConnection, ZmqPullConnection


zf = ZmqFactory()
reciever = None
sink = None
ssh_options = {}


class _CommandTransport(SSHClientTransport):
    _secured = False

    def verifyHostKey(self, hostKey, fingerprint):
        return succeed(True)

    def connectionSecure(self):
        self._secured = True
        command = _CommandConnection(
            self.factory.command,
            self.factory.commandProtocolFactory,
            self.factory.commandConnected)
        userauth = SSHUserAuthClient(
            ssh_options['user'], ConchOptions(), command)
        self.requestService(userauth)

    def connectionLost(self, reason):
        if not self._secured:
            self.factory.commandConnected.errback(reason)


class _CommandConnection(SSHConnection):
    def __init__(self, command, protocolFactory, commandConnected):
        SSHConnection.__init__(self)
        self._command = command
        self._protocolFactory = protocolFactory
        self._commandConnected = commandConnected

    def serviceStarted(self):
        channel = _CommandChannel(
            self._command, self._protocolFactory, self._commandConnected)
        self.openChannel(channel)


class _CommandChannel(SSHChannel):
    name = 'session'

    def __init__(self, command, protocolFactory, commandConnected):
        SSHChannel.__init__(self)
        self._command = command
        self._protocolFactory = protocolFactory
        self._commandConnected = commandConnected

    def openFailed(self, reason):
        self._commandConnected.errback(reason)

    def channelOpen(self, ignored):
        self.conn.sendRequest(self, 'exec', NS(self._command))
        self._protocol = self._protocolFactory.buildProtocol(None)
        self._protocol.makeConnection(self)

    def dataReceived(self, data):
        self._protocol.dataReceived(data)

    def closed(self):
        SSHChannel.closed(self)
        self._protocol.connectionLost(
            Failure(ConnectionDone("ssh channel closed")))
        # must close the transport otherwise connections stay open. \o/
        # this wasn't in the example conch code, lsof -p to the rescue.
        self.conn.transport.loseConnection()


class SSHCommandClientEndpoint(object):
    implements(IStreamClientEndpoint)

    def __init__(self, command, sshServer):
        self._command = command
        self._sshServer = sshServer

    def connect(self, protocolFactory):
        factory = Factory()
        factory.protocol = _CommandTransport
        factory.command = self._command
        factory.commandProtocolFactory = protocolFactory
        factory.commandConnected = Deferred()

        d = self._sshServer.connect(factory)
        d.addErrback(factory.commandConnected.errback)

        return factory.commandConnected


class SinkResultSend(Protocol):

    data = ''

    def dataReceived(self, data):
        self.data += data

    def connectionLost(self, reason):
        self.factory.finished.callback(None)
        res_dict = re.match(r'.*up\s+(?P<uptime>.*?),\s+([0-9]+) users?', self.data.strip()).groupdict()
        sink.push("worker_id: %s, host: %s, result: %s" % (
            ssh_options['worker_id'],
            self.factory._host,
            res_dict['uptime']
        ))


def copyToSinkResult(endpoint):
    resultFactory = Factory()
    resultFactory.protocol = SinkResultSend
    resultFactory.finished = Deferred()
    resultFactory._host = endpoint._sshServer._host
    d = endpoint.connect(resultFactory)
    d.addErrback(resultFactory.finished.errback)
    return resultFactory.finished


def do_ssh(message):
    host = message.pop().strip()
    from twisted.internet import reactor
    from twisted.internet.endpoints import TCP4ClientEndpoint
    sshServer = TCP4ClientEndpoint(reactor, host, ssh_options['port'])
    commandEndpoint = SSHCommandClientEndpoint("uptime", sshServer)
    d = copyToSinkResult(commandEndpoint)
    d.addErrback(err, "ssh command / copy to stdout failed")
    d.addCallback(lambda ignored: ignored)
    return d


if __name__ == '__main__':

    from twisted.python.log import startLogging
    from twisted.internet import reactor
    from txrdq.rdq import ResizableDispatchQueue

    # startLogging(sys.stdout)

    parser = OptionParser("UptimeWorker")
    parser.add_option("-i", "--id", dest="id", help="Worker ID")
    parser.add_option("-p", "--ssh-port", dest="port", help="ssh port")
    parser.add_option("-u", "--ssh-user", dest="user", help="ssh user")
    parser.add_option("-s", "--source", dest="source", help="0MQ ssh hosts producer Endpoint")
    parser.add_option("-r", "--results", dest="results", help="0MQ ssh result sink Endpoint")
    parser.add_option("-c", "--concurrency", dest="concurrency", help="Max concurrent ssh sessions")

    (options, args) = parser.parse_args()
    ssh_options = {
        'worker_id': options.id,
        'port': int(options.port),
        'user': options.user,
    }

    # limit concurrency otherwise things go pear shaped.
    rdq = ResizableDispatchQueue(do_ssh, int(options.concurrency))

    # setup pull socket to ssh host producerr
    hosts_endpont = ZmqEndpoint('connect', options.source)
    reciever = ZmqPullConnection(zf, hosts_endpont)
    reciever.onPull = rdq.put

    # setup result sink socket
    sink_endpoint = ZmqEndpoint('connect', options.results)
    sink = ZmqPushConnection(zf, sink_endpoint)
    reactor.run()
