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
  walk = [ [ {} for j in range(len(maze[0])) ] for i in range(len(maze)) ]
  start = portals['AA'][0]
  walk[start[0]][start[1]][0] = 0
  open_list = [ (start[0], start[1], 0) ]
  while open_list:
    p = open_list.pop(0)
    #print p
    pi, pj, l = p

    if (pi, pj) == portals['ZZ'][0] and l == 0:
      return walk[pi][pj][0]

    neighbors = [ (pi-1, pj, l), (pi+1, pj, l), (pi, pj-1, l), (pi, pj+1, l) ]
    if (pi, pj) in portalneighbors:
      #print 'portalneighbor', p
      pni, pnj = portalneighbors[(pi, pj)]
      if pi in (2, height-2-1) or pj in (2, width-2-1):
        nextlayer = l-1
      else:
        nextlayer = l+1
      neighbors += [ (pni, pnj, nextlayer) ]
    for n in neighbors:
      ni, nj, nl = n
      if maze[ni][nj] == '.' and \
        nl >= 0 and \
        nl not in walk[ni][nj]:
        walk[ni][nj][nl] = walk[pi][pj][l]+1
        open_list += [ (ni, nj, nl) ]


steps = findpath()
print 'Distance: %s' % steps