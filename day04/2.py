#!/usr/bin/env python

from collections import Counter
import sys


passwdrange = None
with open(sys.argv[1]) as f:
  for line in f.readlines():
    passwdrange = [ int(n) for n in line.split('-') ]


filt = []
for i in range(passwdrange[0], passwdrange[1]+1):
  s = str(i)
  adj = [ s[i:i+2] for i in range(len(s)-1) ]
  if any([ d[0] == d[1] for d in adj ]) and \
     all([ d[0] <= d[1] for d in adj ]):
     filt += [ s ]


summa = 0
for s in filt:
  c = Counter(s)
  if 2 in c.values():
    summa += 1


print "The number of passwords that satisfy the criteria: %d" % summa
