#!/usr/bin/env python

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


def walk(pos, keys):
  reachablekeys = {}
  dist = [ [ None for j in range(len(tunnels[0])) ] for i in range(len(tunnels)) ]
  dist[pos[0]][pos[1]] = 0
  open_list = [ pos ]
  neighbors = [ (-1, 0), (1, 0), (0, -1), (0, 1) ]
  while open_list:
    curr_pos = open_list.pop(0)
    for n in neighbors:
      ncell_pos = (curr_pos[0]+n[0], curr_pos[1]+n[1])
      ncell = tunnels[ncell_pos[0]][ncell_pos[1]]
      if ncell == '#' or \
         (ncell.isupper() and ncell.lower() not in keys) or \
         dist[ncell_pos[0]][ncell_pos[1]] != None:
        continue
      d = dist[curr_pos[0]][curr_pos[1]]
      dist[ncell_pos[0]][ncell_pos[1]] = d+1
      if ncell.islower() and ncell not in keys:
        reachablekeys[ncell] = d+1
      else:
        open_list += [ ncell_pos ]

  return reachablekeys


print 'Precalculating distances...'
dists = {}
print 'Calculating for starting position'
dists['@'] = walk(pos, [])
for k, kpos in keys_pos.iteritems():
  print 'Calculating for key [%s]' % k
  dists[k] = walk(kpos, [])



steps = {}
def collectkeys(pos, keys, steps_sofar):
  #print 'Position is %s, having keys [%s]' % (str(pos), ''.join(sorted(keys)))
  reachablekeys = walk(pos, keys)
  #print 'Key data: %s' % reachablekeys
  for newkey, extrasteps in reachablekeys.iteritems():
    collectkeys(keys_pos[newkey], keys+newkey, steps_sofar+extrasteps)

  if len(keys) == len(allkeys):
    steps[keys] = steps_sofar
  #time.sleep(1)


collectkeys(pos, '', 0)
print 'Possible solutions: %s' % steps
minsolution = min(steps, key=lambda k: steps[k])
print 'Shortest solution: %s with %s steps' % (minsolution, steps[minsolution])
