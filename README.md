challenge
=========


Assumptions:

  Actions are case sensitive.
  Numbers are integers, rounding will occur.
  Lines that fail to meet the format requirements are skipped.
  Negative numbers are allowed.

Known bugs:
  None


#sample input:



bearn:challenge bearnard$ cat test1.data 
  SUM: 1, 2, 3 
  MIN: 4, 3, 2, 40
 AVERAGE: 2, 2
  MIN: a4, 3, 2, 40
MIN: 1, 2 3
FOO: 1, 2, 3
MIN:
MIN 112233
  MIN: 4, -3, 2, 40
  MIN: 4, 3, 2, 40
  AVERAGE    : 4, 3, 2, -40
 average    : 4, 3, 2, 40
MIN: 1
MAX: 1
AVERAGE: 1
SUM: 1
SUM: 0
AVERAGE: 0
MAX: 0
MIN: 0



#sample output

bearn:challenge bearnard$ ./test1.py test1.data 
SUM 6
MIN 2
AVERAGE 2
MIN -3
MIN 2
AVERAGE -8
MIN 1
MAX 1
AVERAGE 1
SUM 1
SUM 0
AVERAGE 0
MAX 0
MIN 0

