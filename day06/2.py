#!/usr/bin/env python

from collections import defaultdict
import sys


class Obj(object):
  def __init__(self, name, orbits=None):
    self.name = name
    self.orbits = orbits
    self.orbiters = []

  def __repr__(self):
    return self.name


orbitmap = defaultdict(list)
with open(sys.argv[1]) as f:
  for line in f.readlines():
    a, b = line.strip().split(')')
    orbitmap[a] += [ b ]



root = Obj('COM')
you = None
san = None
def build_tree(curr):
  global you, san
  if curr.name == 'YOU':
    you = curr
  elif curr.name == 'SAN':
    san = curr
  nxts = orbitmap[curr.name]
  for n in nxts:
    curr.orbiters += [ Obj(n, curr) ]
  for n in curr.orbiters:
    build_tree(n)
    

def get_num_orbits(curr, orbits):
  return orbits + sum([ get_num_orbits(n, orbits+1) for n in curr.orbiters ])


build_tree(root)

san_list = []
curr = san
while curr != root:
  san_list += [ curr.orbits ]
  curr = curr.orbits
print "Orbiting list for Santa: %s" % san_list

you_list = []
curr = you
while curr != root:
  you_list += [ curr.orbits ]
  curr = curr.orbits
print "Orbiting list for You:   %s" %you_list


curr = you.orbits
you_common_num = 0
while True:
  if curr in san_list:
    break
  else:
    you_common_num += 1
    curr = curr.orbits

curr = san.orbits
san_common_num = 0
while True:
  if curr in you_list:
    break
  else:
    san_common_num += 1
    curr = curr.orbits


print "Minimal orbital transfers: %d" % (you_common_num + san_common_num)
