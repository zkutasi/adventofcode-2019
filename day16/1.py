#!/usr/bin/env python

from itertools import cycle, repeat
import sys
import time

num = None
with open(sys.argv[1]) as f:
  for line in f.readlines():
    num = [ int(n) for n in line.strip() ]



phasenum = int(sys.argv[2])
for phi in range(1, phasenum+1):
  newnum = []
  for posi in range(len(num)):
    c = cycle( item for sublist in [ list(repeat(e, posi+1)) for e in [0, 1, 0, -1] ] for item in sublist )
    next(c)
    pattern = [ next(c) for i in range(len(num)) ]
    newnum += [ int( str( sum([ e1*e2 for e1,e2 in zip(num, pattern) ]) )[-1] ) ]
  num = newnum
  print "After %d phases: %s" % (phi, ''.join([ str(n) for n in num ])[:8])
