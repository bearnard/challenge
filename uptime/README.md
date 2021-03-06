challenge
=========

Setup:
```
    virtualenv env
    . ./env/bin/activate
    pip install -r requirements.txt
```

Versions:
```

    uptime_multi:
        multiprocessing version, may not be very efficient at high concurency levels

    uptime_gevent:
        More effecient at realy large concurrencies due to minimal context switching 
    
    uptime_multi_queue:
        multiprocessing version (producer/consumer)

            At higher concurrencies forking becomes a problem.

            (env)bearn:uptime bearnard$ time ./uptime_multi_queue.py foo 2500
            Traceback (most recent call last):
              File "./uptime_multi_queue.py", line 50, in <module>
                sshw.start()
              File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/multiprocessing/process.py", line 130, in start
                self._popen = Popen(self)
              File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/multiprocessing/forking.py", line 120, in __init__
                self.pid = os.fork()
            OSError: [Errno 35] Resource temporarily unavailable

            real    0m3.816s
            user    0m1.422s
            sys 0m6.138s



    uptime_gevent_queue:
        gevent version (producer/consumer)
        this should be the most efficient as long as there isn't any blocking code trying to run.
            
            Greenlets are light.

            (env)bearn:uptime bearnard$ time ./uptime_gevent_queue.py foo 2500
            host1.domain.net 64 days, 11:53
            host2.domain.net 64 days, 11:36
            host2.domain.net 64 days, 11:36
            host2.domain.net 64 days, 11:36
            host1.domain.net 64 days, 11:53
            host2.domain.net 64 days, 11:36
            host1.domain.net 64 days, 11:53
            host1.domain.net 64 days, 11:53
            host3.domain.net 64 days, 11:32
            host2.domain.net 64 days, 11:36
            host2.domain.net 64 days, 11:36
            host2.domain.net 64 days, 11:36
            host1.domain.net 64 days, 11:53
            host1.domain.net 64 days, 11:53
            host2.domain.net 64 days, 11:36
            host1.domain.net 64 days, 11:53
            host2.domain.net 64 days, 11:36
            host1.domain.net 64 days, 11:53
            host1.domain.net 64 days, 11:53

            real    0m1.607s
            user    0m0.652s
            sys 0m0.085s

    bash:
        cat foo |xargs -n1 -P 20 bash  -c 'resp=$(ssh $1 "uptime"|cut -f 4-6 -d " ") ;echo  "$1 - $resp" ' _


```

References:
```
    http://sdiehl.github.com/gevent-tutorial/
    http://www.doughellmann.com/PyMOTW/multiprocessing/basics.html
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
(env)bearn:uptime bearnard$ time cat foo |xargs -n1 -P 20 bash  -c 'resp=$(ssh $1 "uptime"|cut -f 4-6 -d " ") ;echo  "$1 - $resp" ' _
host2.domain.net 63 days, 18:06,
host2.domain.net 63 days, 18:06,
host2.domain.net 63 days, 18:06,
host1.domain.net 63 days, 18:23,
host1.domain.net 63 days, 18:23,
host1.domain.net 63 days, 18:23,
host1.domain.net 63 days, 18:23,
host1.domain.net 63 days, 18:23,
host2.domain.net 63 days, 18:06,
host2.domain.net 63 days, 18:06,
host2.domain.net 63 days, 18:06,
host2.domain.net 63 days, 18:06,
host1.domain.net 63 days, 18:23,
host1.domain.net 63 days, 18:23,
host3.domain.net 63 days, 18:02,
host1.domain.net 63 days, 18:23,
host1.domain.net 63 days, 18:23,
host2.domain.net 63 days, 18:06,
host2.domain.net 63 days, 18:06,

real    0m1.854s
user    0m0.421s
sys 0m0.219s


(env)bearn:uptime bearnard$ cat foo 
host1.domain.net
host2.domain.net
host3.domain.net
host4.domain.net
host5.domain.net
```


#sample output
```



(env)bearn:uptime bearnard$ time ./uptime_gevent_queue.py foo 25
host1.domain.net 63 days, 17:48
host2.domain.net 63 days, 17:31
host2.domain.net 63 days, 17:31
host2.domain.net 63 days, 17:31
host1.domain.net 63 days, 17:48
host1.domain.net 63 days, 17:48
host1.domain.net 63 days, 17:48
host3.domain.net 63 days, 17:27
host1.domain.net 63 days, 17:48
host1.domain.net 63 days, 17:48
host1.domain.net 63 days, 17:48
host2.domain.net 63 days, 17:31
host2.domain.net 63 days, 17:31
host2.domain.net 63 days, 17:31
host1.domain.net 63 days, 17:48
host1.domain.net 63 days, 17:48
host2.domain.net 63 days, 17:31
host2.domain.net 63 days, 17:31
host2.domain.net 63 days, 17:31

real    0m1.682s
user    0m0.757s
sys 0m0.082s
(env)bearn:uptime bearnard$ time ./uptime_multi_queue.py foo 25
host1.domain.net 63 days, 17:48
host1.domain.net 63 days, 17:48
host1.domain.net 63 days, 17:48
host2.domain.net 63 days, 17:31
host2.domain.net 63 days, 17:31
host2.domain.net 63 days, 17:31
host1.domain.net 63 days, 17:48
host2.domain.net 63 days, 17:31
host1.domain.net 63 days, 17:48
host1.domain.net 63 days, 17:48
host1.domain.net 63 days, 17:48
host2.domain.net 63 days, 17:31
host2.domain.net 63 days, 17:31
host2.domain.net 63 days, 17:31
host2.domain.net 63 days, 17:31
host2.domain.net 63 days, 17:31
host1.domain.net 63 days, 17:48
host3.domain.net 63 days, 17:27
host1.domain.net 63 days, 17:48

real    0m2.090s
user    0m1.083s
sys 0m0.322s
```
