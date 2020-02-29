#!/usr/bin/env python

from collections import defaultdict
import sys
import time

tunnels = []
allkeys = set()

with open(sys.argv[1]) as f:
  for line in f.readlines():
    tunnels += [ line ]
    allkeys |= set([ e for e in line if e.islower() ])

height = len(tunnels)
width = len(tunnels[0])
pos = None
keys_pos = {}
for i in range(height):
  for j in range(width):
    if tunnels[i][j] == '@':
      pos = (i,j)
    elif tunnels[i][j].islower():
      keys_pos[tunnels[i][j]] = (i,j)
print "All the keys: [%s] (%s pieces), positions: %s" % (''.join(sorted(allkeys)), len(allkeys), str(keys_pos))


def print_tunnel(tun):
  h = len(tun)
  w = len(tun[0])
  print "   %s" % ''.join([ str(s / 10) if s>10 else ' ' for s in range(w) ])
  print "   %s" % ''.join([ str(s % 10) for s in range(w) ])
  for y in range(h):
    print "%2d %s" % (y, ''.join([ str(e%10) if e is not None else '?'for e in tun[y] ]))
  print


def freewalk(pos):
  reachablekeys = {}
  dist = [ [ [None, None] for j in range(len(tunnels[0])) ] for i in range(len(tunnels)) ]
  dist[pos[0]][pos[1]] = [0, '']
  open_list = [ pos ]
  neighbors = [ (-1, 0), (1, 0), (0, -1), (0, 1) ]
  while open_list:
    curr_pos = open_list.pop(0)
    for n in neighbors:
      ncell_pos = (curr_pos[0]+n[0], curr_pos[1]+n[1])
      ncell = tunnels[ncell_pos[0]][ncell_pos[1]]
      if ncell == '#' or \
         dist[ncell_pos[0]][ncell_pos[1]][0] != None:
        continue
      d, doors = dist[curr_pos[0]][curr_pos[1]]
      open_list += [ ncell_pos ]
      if ncell.isupper():
        doors += ncell
      dist[ncell_pos[0]][ncell_pos[1]] = [d+1, doors]
      if ncell.islower():
        reachablekeys[ncell] = (d+1, doors)
        

  return reachablekeys


print 'Precalculating distances...'
dists = {}
print 'Calculating for starting position'
dists['@'] = freewalk(pos)
print 'Results: %s' % (dists['@'])
for k, kpos in keys_pos.iteritems():
  print 'Calculating for key [%s]' % k
  dists[k] = freewalk(kpos)
  print 'Results from key [%s]: %s' % (k, dists[k])


steps = {}
memo = {}
def collectkeys(pos, keys, steps_sofar):
  sortedkeys = ''.join(sorted(keys))
  if (pos, sortedkeys) in memo and memo[(pos, sortedkeys)] <= steps_sofar:
    return
  else:
    memo[(pos, sortedkeys)] = steps_sofar

  #print pos, keys, steps_sofar
  #time.sleep(0.02)
  reachablekeys = dists[pos]
  for newkey, data in reachablekeys.iteritems():
    extrasteps, doors = data
    if all([ d.lower() in keys for d in doors ]) and newkey not in keys:
      collectkeys(newkey, keys+newkey, steps_sofar+extrasteps)

  if len(keys) == len(allkeys):
    steps[keys] = steps_sofar


collectkeys('@', '', 0)
print 'Possible solutions: %s' % steps
minsolution = min(steps, key=lambda k: steps[k])
print 'Shortest solution: %s with %s steps' % (minsolution, steps[minsolution])
