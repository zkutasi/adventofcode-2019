#!/usr/bin/env python

from collections import defaultdict
import re
import sys

rgx = re.compile('[A-Z]{2}')

maze = []
with open(sys.argv[1]) as f:
  for line in f.readlines():
    maze += [ line.replace('\n', '') ]


portals = defaultdict(list)
height = len(maze)
width = len(maze[0])
for i in range(2, height-2):
  for j in range(2, width-2):
    up = maze[i-2][j]+maze[i-1][j]
    if maze[i][j] == '.' and rgx.match(up):
      portals[up] += [ (i,j) ]

    down = maze[i+1][j]+maze[i+2][j]
    if maze[i][j] == '.' and rgx.match(down):
      portals[down] += [ (i,j) ]

    left = maze[i][j-2]+maze[i][j-1]
    if maze[i][j] == '.' and rgx.match(left):
      portals[left] += [ (i,j) ]

    right = maze[i][j+1]+maze[i][j+2]
    if maze[i][j] == '.' and rgx.match(right):
      portals[right] += [ (i,j) ]

print 'Portals: %s' % portals
portalneighbors = {}
for portal, positions in portals.iteritems():
  if len(positions) == 1:
    continue
  p1 = positions[0]
  p2 = positions[1]
  portalneighbors[p1] = p2
  portalneighbors[p2] = p1


def findpath():
  walk = [ [ None for j in range(len(maze[0])) ] for i in range(len(maze)) ]
  start = portals['AA'][0]
  walk[start[0]][start[1]] = 0
  open_list = [ start ]
  while open_list:
    p = open_list.pop(0)
    pi, pj = p

    if p == portals['ZZ'][0]:
      return walk[pi][pj]

    neighbors = [ (pi-1, pj), (pi+1, pj), (pi, pj-1), (pi, pj+1) ]
    if p in portalneighbors:
      neighbors += [ portalneighbors[p] ]
    for n in neighbors:
      ni, nj = n
      if maze[ni][nj] == '.' and \
        walk[ni][nj] is None:
        walk[ni][nj] = walk[pi][pj]+1
        open_list += [ n ]


steps = findpath()
print 'Distance: %s' % steps