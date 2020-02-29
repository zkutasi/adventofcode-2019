#!/usr/bin/env python

from collections import defaultdict
import sys
import time

tunnels = []
allkeys = set()

with open(sys.argv[1]) as f:
  for line in f.readlines():
    tunnels += [ list(line) ]
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


tunnels[pos[0]][pos[1]] = '#'
tunnels[pos[0]-1][pos[1]] = '#'
tunnels[pos[0]+1][pos[1]] = '#'
tunnels[pos[0]][pos[1]-1] = '#'
tunnels[pos[0]][pos[1]+1] = '#'
tunnels[pos[0]-1][pos[1]-1] = '@'
tunnels[pos[0]-1][pos[1]+1] = '@'
tunnels[pos[0]+1][pos[1]-1] = '@'
tunnels[pos[0]+1][pos[1]+1] = '@'
pos1 = (pos[0]-1, pos[1]-1)
pos2 = (pos[0]-1, pos[1]+1)
pos3 = (pos[0]+1, pos[1]-1)
pos4 = (pos[0]+1, pos[1]+1)


def print_tunnel(tun):
  h = len(tun)
  w = len(tun[0])
  print "   %s" % ''.join([ str(s / 10) if s>10 else ' ' for s in range(w) ])
  print "   %s" % ''.join([ str(s % 10) for s in range(w) ])
  for y in range(h):
    print "%2d %s" % (y, ''.join([ str(e[0]%10) if e[0] is not None else '?' for e in tun[y] ]))
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
        
  #print_tunnel(dist)
  return reachablekeys


print 'Precalculating distances...'
dists = {}
print 'Calculating for starting positions'
dists['@'] = [
  None,
  freewalk(pos1),
  freewalk(pos2),
  freewalk(pos3),
  freewalk(pos4)
]
print 'Results: %s' % (dists['@'][1:])
for k, kpos in keys_pos.iteritems():
  print 'Calculating for key [%s]' % k
  data = freewalk(kpos)
  dists[k] = [ None, data, data, data, data ]
  print 'Results from key [%s]: %s' % (k, dists[k][1:])


minsolution = ( None, float('inf') )
memo = {}
def collectkeys(pos1, pos2, pos3, pos4, keys, steps_sofar):
  global minsolution
  if steps_sofar >= minsolution[1]:
    return

  sortedkeys = ''.join(sorted(keys))
  if (pos1, pos2, pos3, pos4, sortedkeys) in memo and \
      memo[(pos1, pos2, pos3, pos4, sortedkeys)] <= steps_sofar:
    return
  else:
    memo[(pos1, pos2, pos3, pos4, sortedkeys)] = steps_sofar

  reachablekeys1 = dists[pos1][1]
  reachablekeys2 = dists[pos2][2]
  reachablekeys3 = dists[pos3][3]
  reachablekeys4 = dists[pos4][4]
  for newkey, data in reachablekeys1.iteritems():
    extrasteps, doors = data
    if all([ d.lower() in keys for d in doors ]) and newkey not in keys:
      collectkeys(newkey, pos2, pos3, pos4, keys+newkey, steps_sofar+extrasteps)
  for newkey, data in reachablekeys2.iteritems():
    extrasteps, doors = data
    if all([ d.lower() in keys for d in doors ]) and newkey not in keys:
      collectkeys(pos1, newkey, pos3, pos4, keys+newkey, steps_sofar+extrasteps)
  for newkey, data in reachablekeys3.iteritems():
    extrasteps, doors = data
    if all([ d.lower() in keys for d in doors ]) and newkey not in keys:
      collectkeys(pos1, pos2, newkey, pos4, keys+newkey, steps_sofar+extrasteps)
  for newkey, data in reachablekeys4.iteritems():
    extrasteps, doors = data
    if all([ d.lower() in keys for d in doors ]) and newkey not in keys:
      collectkeys(pos1, pos2, pos3, newkey, keys+newkey, steps_sofar+extrasteps)

  if len(keys) == len(allkeys) and steps_sofar < minsolution[1]:
    minsolution = (keys, steps_sofar)


collectkeys('@', '@', '@', '@', '', 0)
print 'Shortest solution: %s with %s steps' % minsolution
