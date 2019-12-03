#!/usr/bin/env python

import sys

wires = {
  0: None,
  1: None
}

with open(sys.argv[1]) as f:
  i = 0
  for line in f.readlines():
    wires[i] = [ ( w[0], int(w[1:]) ) for w in line.split(',') ]
    i += 1


xmax = 0
xmin = 0
ymax = 0
ymin = 0
for i in [0, 1]:
  xact = 0
  yact = 0
  for d, l in wires[i]:
    if d in 'LR':
      if d == 'L':
        xact -= l
        xmin = min(xact, xmin)
      else:
        xact += l
        xmax = max(xact, xmax)
    elif d in 'UD':
      if d == 'U':
        yact -= l
        ymin = min(yact, ymin)
      else:
        yact += l
        ymax = max(yact, ymax)

print "Calculated size of board: x=[%d, %d], y=[%d, %d]" % (xmin, xmax, ymin, ymax)

h = ymax - ymin
w = xmax - xmin
board = [ [ 0 for y in range(h + 1) ] for x in range(w + 1) ]


centralx = None
centraly = None
intersections = []
for i in [0, 1]:
  sumdist = 1
  xact = -xmin
  yact = -ymin
  board[xact][yact] = 'o'
  centralx = xact
  centraly = yact
  for d, l in wires[i]:
    while l>0:
      if d == 'L':
        xact -= 1
      elif d == 'R':
        xact += 1
      elif d == 'U':
        yact -= 1
      elif d == 'D':
        yact += 1
      if i == 0:
        board[xact][yact] = sumdist
      if i == 1 and board[xact][yact] > 0:
        intersections += [ board[xact][yact] + sumdist ]
      sumdist += 1
      l -= 1


print "The closest intersection's distance is: %d" % min(intersections)
