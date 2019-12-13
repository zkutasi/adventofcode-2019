#!/usr/bin/env python

from itertools import combinations
import re
import sys

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
  print "Energy after %d steps:" % steps
  totalenergy = 0
  for m in moons:
    pot = m.get_pot()
    kin = m.get_kin()
    print "pot: %d; kin: %d; total: %d" % (pot, kin, pot*kin)
    totalenergy += pot*kin
  print "Sum of total energy: %d" % totalenergy
  print "-------------------------------------"


steps = int(sys.argv[2])
print_state(0)
for s in range(1, steps+1):
  for a,b in combinations(moons, 2):
    for dim in [0,1,2]:
      if a.pos[dim] < b.pos[dim]:
        a.vel[dim] += 1
        b.vel[dim] -= 1
      elif a.pos[dim] > b.pos[dim]:
        a.vel[dim] -= 1
        b.vel[dim] += 1

  for m in moons:
    for dim in [0,1,2]:
      m.pos[dim] += m.vel[dim]

  

  print_state(s)
