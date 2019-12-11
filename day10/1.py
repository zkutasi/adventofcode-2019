#!/usr/bin/env python

import math
import sys


asteroidmap = []
with open(sys.argv[1]) as f:
  for line in f.readlines():
    asteroidmap += [ list(line.strip()) ]


height = len(asteroidmap)
width = len(asteroidmap[0])


def print_map(m):
  h = len(m)
  w = len(m[0])
  print "   %s" % ''.join([ str(s / 10) if s>10 else ' ' for s in range(w) ])
  print "   %s" % ''.join([ str(s % 10) for s in range(w) ])
  for y in range(h):
    print "%2d %s" % (y, ''.join(m[y]))
  print



def print_viewmap(m):
  h = len(m)
  w = len(m[0])
  print "   %s" % ''.join([ str(s / 10) if s>10 else ' ' for s in range(w) ])
  print "   %s" % ''.join([ str(s % 10) for s in range(w) ])
  for y in range(h):
    print "%2d %s" % (y, ''.join([ (str(e if e<10 else 'M') if e is not None else '.') for e in m[y] ]))
  print


def is_integer(num):
  tolerance = 0.00000001
  return abs(num - round(num)) < tolerance


def has_direct_sight(a, b, debug=False):
  if debug:
    print "DBG :", a, b
  result = True
  if a[0] == b[0]:
    px = a[0]
    if a[1] < b[1]:
      inc = 1
    else:
      inc = -1
    for py in range(a[1]+inc, b[1], inc):
      if asteroidmap[py][px] == '#':
        result = False
  else:
    m = float(b[1]-a[1])/(b[0]-a[0])
    c = float(a[1]) - m*a[0]
    if a[0] < b[0]:
      inc = 1
    else:
      inc = -1
    for px in range(a[0]+inc, b[0], inc):
      py = m*px + c
      if debug:
        print "DBG :", px, repr(py), round(py), asteroidmap[int(py)][px]
      if is_integer(py) and asteroidmap[int(round(py))][px] == '#':
        result = False

  return result


def has_direct_sight2(a, b, debug=False):
  if debug:
    print "DBG2:", a, b
  result = True
  if a[0] == b[0]:
    px = a[0]
    if a[1] < b[1]:
      inc = 1
    else:
      inc = -1
    for py in range(a[1]+inc, b[1], inc):
      if asteroidmap[py][px] == '#':
        result = False
  else:
    if a[0] < b[0]:
      inc = 1
    else:
      inc = -1
    for px in range(a[0]+inc, b[0], inc):
      py_size = float(abs(px-a[0])*abs(a[1]-b[1]))/abs(a[0]-b[0])
      if a[1] < b[1]:
        py = a[1] + py_size
      else:
        py = a[1] - py_size
      if debug:
        print "DBG2:", px, repr(py), py.is_integer(), asteroidmap[int(py)][px]
      if py.is_integer() and asteroidmap[int(round(py))][px] == '#':
        result = False

  return result



print_map(asteroidmap)

num_asteroids = sum([ row.count('#') for row in asteroidmap ])
print "Number of asteroids: %d" % num_asteroids

viewmap = [ [ None for x in range(width) ] for y in range(height) ]


for x1 in range(width):
  for y1 in range(height):
    if asteroidmap[y1][x1] != '#':
      continue
    viewmap[y1][x1] = num_asteroids-1
    for x2 in range(width):
      for y2 in range(height):
        if asteroidmap[y2][x2] != '#':
          continue
        if x1 == x2 and y1 == y2:
          continue
        direct = has_direct_sight((x1, y1), (x2, y2))
        direct2 = has_direct_sight2((x1, y1), (x2, y2))
        if direct != direct2:
          print "ERROR", direct, direct2
          has_direct_sight((x1, y1), (x2, y2), True)
          has_direct_sight2((x1, y1), (x2, y2), True)
        if not direct2:
          viewmap[y1][x1] -= 1


#print_viewmap(viewmap)

best = (float('-inf'), None, None)
for x in range(width):
  for y in range(height):
    if viewmap[y][x] is None:
      continue
    if viewmap[y][x] > best[0]:
      best = (viewmap[y][x], x, y)

print "The best location for the monitoring station: %s, detecting %d asteroids" % ((best[1], best[2]), best[0])
