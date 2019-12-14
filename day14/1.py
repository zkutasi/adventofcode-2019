#!/usr/bin/env python

from collections import defaultdict
import math
import random
import sys
import time

rules = {}
with open(sys.argv[1]) as f:
  for line in f.readlines():
    left, right = [ e.strip() for e in line.strip().split('=>') ]
    left = [ part.strip().split() for part in left.strip().split(',') ]
    leftelems = {}
    for e in left:
      a, b = e
      leftelems[b] = int(a)
    right = [ part for part in right.strip().split() ]
    a,b = right
    rightelems = (int(a), b)
    if rightelems[1] not in [ rk[1] for rk,rv in rules.items() ]:
      rules[rightelems] = leftelems
    else:
      print "Duplicate rule found"


factory = defaultdict(lambda: 0)
factory["FUEL"] = 1
while any([ v>0 for k,v in factory.items() if k != 'ORE' ]):
  item = random.choice([ (ek,ev) for ek, ev in factory.items() if ev>0 and ek != "ORE" ])
  print "Chosen item %s" % str(item)
  k, v = item
  rulekey, rulevalue = [ (rk,rv) for rk,rv in rules.items() if rk[1] == k ][0]
  amount = int( math.ceil(float(v)/rulekey[0]) )
  print "Amount: %d" % amount
  factory[k] -= rulekey[0] * amount
  for ek, ev in rulevalue.items():
    factory[ek] += amount * ev
  print "Factory content: %s" % [ (k,v) for k,v in factory.items() if v>0 ]
