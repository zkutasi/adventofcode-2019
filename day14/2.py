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



def generate_fuel(fuel_amount):
  factory = defaultdict(lambda: 0)
  factory["FUEL"] = fuel_amount
  while any([ v>0 for k,v in factory.items() if k != 'ORE' ]):
    item = random.choice([ (ek,ev) for ek, ev in factory.items() if ev>0 and ek != "ORE" ])
    k, v = item
    rulekey, rulevalue = [ (rk,rv) for rk,rv in rules.items() if rk[1] == k ][0]
    amount = int( math.ceil(float(v)/rulekey[0]) )
    factory[k] -= rulekey[0] * amount
    for ek, ev in rulevalue.items():
      factory[ek] += amount * ev

  return factory["ORE"]



trillion = 1000000000000
f = 1
ore = 0
while ore < trillion:
  f *= 2
  ore = generate_fuel(f)

print "Anwer is between %d and %d" % (f/2, f)
ore1 = ore2 = 0
interval = [ f/2, f ]
while interval[1] - interval[0] > 1:
  f1 = interval[0] + (interval[1] - interval[0])/2
  f2 = f1 + 1
  ore1 = generate_fuel(f1)
  ore2 = generate_fuel(f2)
  if ore1 < trillion and ore2 < trillion:
    interval[0] = f1
  elif ore1 < trillion and ore2 > trillion:
    interval = [ f1, f2 ]
    break
  elif ore1 > trillion and ore2 > trillion:
    interval[1] = f2


print "Maximum fuel possible with 1 trillion ORE is %s" % interval[0]
