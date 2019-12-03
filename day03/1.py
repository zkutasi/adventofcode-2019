#!/usr/bin/env python

import sys

wires = {
  1: None,
  2: None
}

with open(sys.argv[1]) as f:
  i = 1
  for line in f.readlines():
    wires[i] = [ ( w[0], int(w[1:]) ) for w in line.split(',') ]
    i += 1


xmax = 0
xmin = 0
ymax = 0
ymin = 0
for i in [1, 2]:
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

MARGIN = 1
h = ymax - ymin
w = xmax - xmin
board = [ [ '.' for y in range(h + 1 + 2*MARGIN) ] for x in range(w + 1 + 2*MARGIN) ]

def print_board():
  print "  %s" % ''.join( [ str(x/10 % 10) if x/10>0 else ' ' for x in range(len(board)) ] )
  print "  %s" %''.join( [ str(x % 10) for x in range(len(board)) ] )
  for y in range(len(board[0])):
    print "%2d%s" % ( y, ''.join( [ board[x][y] for x in range(len(board)) ] ) )
  print


centralx = None
centraly = None
intersections = []
for i in [1, 2]:
  xact = -xmin + MARGIN
  yact = -ymin + MARGIN
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
      if i == 2 and board[xact][yact] == '1':
        board[xact][yact] = 'X'
        intersections += [ (xact, yact) ]
      else:
        board[xact][yact] = str(i)
      l -= 1


#print_board()

best = float("inf")
for x,y in intersections:
  best = min(abs(x-centralx)+abs(y-centraly), best)


print "The closest intersection's distance is: %d" % best
