Distributed uptime via zeromq.
=========

Setup:
```
    virtualenv env
    . ./env/bin/activate
    pip install -r requirements.txt
```

Details:
```

    sender.py:
        sends hosts to all connected workers (round-robin)

            (env)bearn:uptime_gevent_zmq bearnard$ python sender.py 
            Usage: sender.py filename watermark_limit

    worker.py:
        gevent ssh uptime worker, sends results to the result sink

            (env)bearn:uptime_gevent_zmq bearnard$ python worker.py 
            Usage: worker.py worker_id concurrency    
        
            to be run on multiple nodes....

    result_sink.py:
        consumes uptime results, prints to stdout and writes to a file.

            (env)bearn:uptime_gevent_zmq bearnard$ python result_sink.py 
            Usage: result_sink.py filename

```

References:
```
    http://sdiehl.github.com/gevent-tutorial/
    http://zeromq.github.com/pyzmq/index.html
    https://github.com/traviscline/gevent-zeromq
```

Assumptions:
```
  Port 22
  no input validation
  Each line is a valid ssh host
  a valid ssh key is required for each host and is loaded into your keychain
```
Known bugs:
```
  None
```

#sample input:


```
(env)bearn:uptime bearnard$ cat foo 
host1.domain.net
host2.domain.net
host3.domain.net
host4.domain.net
host5.domain.net
```


#sample output
```

    (env)bearn:uptime_gevent_zmq bearnard$ python sender.py foo 20
    Sending ssh hosts to workers...
    (env)bearn:uptime_gevent_zmq bearnard$ python sender.py foo 20
    Sending ssh hosts to workers...


    (env)bearn:uptime_gevent_zmq bearnard$ python worker.py worker1 20
    Recieved Host: bzz
    Recieved Host: hostX.domain.net
    Recieved Host: hostX.domain.net
    Recieved Host: hostX.domain.net
    Recieved Host: hostX.domain.net
    Recieved Host: hostX.domain.net
    Recieved Host: hostX.domain.net
    Recieved Host: hostX.domain.net
    Recieved Host: hostX.domain.net
    Recieved Host: hostX.domain.net
    Recieved Host: hostX.domain.net
    Recieved Host: hostX.domain.net
    Recieved Host: hostX.domain.net
    Recieved Host: hostX.domain.net


    (env)bearn:uptime_gevent_zmq bearnard$ python result_sink.py res.out
    worker_id: worker1_19, host: bzz, error: [Errno 8] nodename nor servname provided, or not known
    worker_id: worker1_15, host: hostX.domain.net, result: 65 days, 17:07
    worker_id: worker1_16, host: hostX.domain.net, result: 18:15
    worker_id: worker1_7, host: hostX.domain.net, result: 13 days,  5:32
    worker_id: worker1_19, host: hostX.domain.net, result: 176 days, 15:26
    worker_id: worker1_7, host: hostX.domain.net, result: 21 days, 20:09
    worker_id: worker1_15, host: hostX.domain.net, result: 28 days, 11:17
    worker_id: worker1_19, host: hostX.domain.net, result: 20 days, 12:51
    worker_id: worker1_15, host: hostX.domain.net, result: 13 days,  5:32
    worker_id: worker1_19, host: hostX.domain.net, result: 9 days, 16:47
    worker_id: worker1_7, host: hostX.domain.net, result: 1 day,  9:39


```
