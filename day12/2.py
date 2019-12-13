#!/usr/bin/env python

from fractions import gcd
from itertools import combinations
import re
import sys
import time

rgx = re.compile('<x=(\S+), y=(\S+), z=(\S+)>')


class Moon(object):
  def __init__(self, x, y, z):
    self.pos = [x,y,z]
    self.vel = [0,0,0]

  def get_pot(self):
    return sum( [abs(e) for e in self.pos ] )

  def get_kin(self):
    return sum( [abs(e) for e in self.vel ] )


moons = []
with open(sys.argv[1]) as f:
  for line in f.readlines():
    x, y, z = rgx.split(line.strip())[1:-1]
    moons += [ Moon( int(x), int(y), int(z) ) ]


def print_state(steps):
  print "After %d steps:" % steps
  for m in moons:
    print "pos=%s, vel=%s" % (m.pos, m.vel)
  print


print_state(0)

found = [ False, False, False ]
periods = []
s = 1
while not all(found):
  for a,b in combinations(moons, 2):
    for dim in [0,1,2]:
      if a.pos[dim] < b.pos[dim]:
        a.vel[dim] += 1
        b.vel[dim] -= 1
      elif a.pos[dim] > b.pos[dim]:
        a.vel[dim] -= 1
        b.vel[dim] += 1

  for mi, m in enumerate(moons):
    for dim in [0,1,2]:
      m.pos[dim] += m.vel[dim]

  for dim in [0,1,2]:
    if all([ m.vel[dim] == 0 for m in moons ]) and not found[dim]:
      print "Period of axis %d is %d" % (dim, s)
      found[dim] = True
      periods += [ s ]
      print_state(s)
  s += 1



def lcm(x, y):
  return x * y // gcd(x, y)

print 2*reduce(lcm, periods)
