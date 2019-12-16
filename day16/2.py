#!/usr/bin/env python

from itertools import cycle, repeat
import sys
import time


repeat = 10000

num = None
with open(sys.argv[1]) as f:
  for line in f.readlines():
    num = [ int(n) for n in line.strip() ] * repeat
lnum = len(num)



offset = int( ''.join([ str(n) for n in num[:7] ]) )
print "Offset is %d" % offset
phasenum = int(sys.argv[2])





def solve():
  for phi in range(1, phasenum+1):
    newnum = list(num)
    rollingsum = 0
    for i in range(len(num)-1, len(num)/2-1, -1):
      rollingsum = abs(rollingsum + num[i]) % 10
      newnum[i] = rollingsum
    num = newnum
    print "After %d phases: %s" % (phi, ''.join([ str(n) for n in num[offset:offset+8] ]))



def solve2():
  for phi in xrange(1, phasenum+1):
    rollingsum = 0
    for i in xrange(lnum-1, lnum/2-1, -1):
      rollingsum = rollingsum + num[i]
      if rollingsum > 10:
        rollingsum -= 10
      num[i] = rollingsum
    print "After %d phase..." % phi
  print "After %d phases: %s" % (phi, ''.join([ str(n) for n in num[offset:offset+8] ]))


solve2()
