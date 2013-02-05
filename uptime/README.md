challenge
=========

Versions:
```

    uptime_multi:
        multiprocessing version, may not be very efficient at high concurency levels

    uptime_gevent:
        More effecient at realy large concurrencies due to minimal context switching 


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
host1.domain.com
host2.domain.com
host3.domain.com
host4.domain.com
host5.domain.com
```


#sample output
```
(env)bearn:uptime bearnard$ time ./uptime_gevent.py foo
/Users/bearnard/Source-Dev/amz_ssh/env/lib/python2.7/site-packages/paramiko/client.py:96: UserWarning: Unknown ssh-rsa host key for [foo2.domain.net]:24: 4298065cc81a5f857ec6c3d5475a56bf
  (key.get_name(), hostname, hexlify(key.get_fingerprint())))
/Users/bearnard/Source-Dev/amz_ssh/env/lib/python2.7/site-packages/paramiko/client.py:96: UserWarning: Unknown ssh-rsa host key for [foo1.domain.net]:24: 4ffc117d879ba575c10fd815db1baecb
  (key.get_name(), hostname, hexlify(key.get_fingerprint())))
Host: foo1.domain.net Response: %s  17:45:38 up 63 days,  6:43,  0 users,  load average: 0.43, 0.53, 0.52

Host: foo2.domain.net Response: %s  17:45:38 up 63 days,  6:26,  0 users,  load average: 0.22, 0.19, 0.15

Host: foo1.domain.net Response: %s  17:45:38 up 63 days,  6:43,  0 users,  load average: 0.43, 0.53, 0.52

Host: foo2.domain.net Response: %s  17:45:38 up 63 days,  6:26,  0 users,  load average: 0.22, 0.19, 0.15

Host: foo1.domain.net Response: %s  17:45:38 up 63 days,  6:43,  0 users,  load average: 0.43, 0.53, 0.52

Host: foo2.domain.net Response: %s  17:45:38 up 63 days,  6:26,  0 users,  load average: 0.22, 0.19, 0.15

Host: foo1.domain.net Response: %s  17:45:38 up 63 days,  6:43,  0 users,  load average: 0.43, 0.53, 0.52

Host: foo2.domain.net Response: %s  17:45:38 up 63 days,  6:26,  0 users,  load average: 0.22, 0.19, 0.15

Host: foo1.domain.net Response: %s  17:45:38 up 63 days,  6:43,  0 users,  load average: 0.43, 0.53, 0.52

Host: foo2.domain.net Response: %s  17:45:38 up 63 days,  6:26,  0 users,  load average: 0.22, 0.19, 0.15

Host: foo1.domain.net Response: %s  17:45:38 up 63 days,  6:43,  0 users,  load average: 0.43, 0.53, 0.52

Host: foo2.domain.net Response: %s  17:45:38 up 63 days,  6:26,  0 users,  load average: 0.22, 0.19, 0.15

Host: foo1.domain.net Response: %s  17:45:38 up 63 days,  6:43,  0 users,  load average: 0.43, 0.53, 0.52

Host: foo2.domain.net Response: %s  17:45:38 up 63 days,  6:26,  0 users,  load average: 0.22, 0.19, 0.15

Host: foo1.domain.net Response: %s  17:45:38 up 63 days,  6:43,  0 users,  load average: 0.43, 0.53, 0.52

Host: foo2.domain.net Response: %s  17:45:38 up 63 days,  6:26,  0 users,  load average: 0.22, 0.19, 0.15

Host: foo1.domain.net Response: %s  17:45:38 up 63 days,  6:43,  0 users,  load average: 0.43, 0.53, 0.52

Host: foo2.domain.net Response: %s  17:45:38 up 63 days,  6:26,  0 users,  load average: 0.22, 0.19, 0.15

Host: foo1.domain.net Response: %s  17:45:38 up 63 days,  6:43,  0 users,  load average: 0.43, 0.53, 0.52


real    0m1.477s
user    0m0.525s
sys 0m0.072s
```
