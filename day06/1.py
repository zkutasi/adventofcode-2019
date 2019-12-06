#!/usr/bin/env python

from collections import defaultdict
import sys


class Obj(object):
  def __init__(self, name):
    self.name = name
    self.orbiters = []

  def __repr__(self):
    return "%s ) %s" % (self.name, [ s.name for s in self.orbiters ])


orbitmap = defaultdict(list)
with open(sys.argv[1]) as f:
  for line in f.readlines():
    a, b = line.strip().split(')')
    orbitmap[a] += [ b ]



def build_tree(curr):
  nxts = orbitmap[curr.name]
  for n in nxts:
    curr.orbiters += [ Obj(n) ]
  for n in curr.orbiters:
    build_tree(n)
    

def get_num_orbits(curr, orbits):
  return orbits + sum([ get_num_orbits(n, orbits+1) for n in curr.orbiters ])


root = Obj('COM')
build_tree(root)
print "Total orbits: %d" % get_num_orbits(root, 0)
