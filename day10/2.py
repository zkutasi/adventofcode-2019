#!/usr/bin/env python

import math
import sys
import time


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


def is_asteroid(x, y):
  return asteroidmap[y][x] in ['#', 'X']


def print_viewmap(m):
  h = len(m)
  w = len(m[0])
  print "   %s" % ''.join([ str(s / 10) if s>10 else ' ' for s in range(w) ])
  print "   %s" % ''.join([ str(s % 10) for s in range(w) ])
  for y in range(h):
    print "%2d %s" % (y, ''.join([ (str(len(e) if len(e)<10 else 'M') if e is not None else '.') for e in m[y] ]))
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
      if is_asteroid(px, py):
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
      if is_integer(py) and is_asteroid(px, int(round(py))):
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
      if is_asteroid(px, py):
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
      if py.is_integer() and is_asteroid(px, int(round(py))):
        result = False

  return result



def fill_viewmap_for_asteroid(x1, y1):
  for x2 in range(width):
    for y2 in range(height):
      if not is_asteroid(x2, y2):
        continue
      if x1 == x2 and y1 == y2:
        viewmap[y1][x1].remove( (x2,y2) )
        continue
      direct = has_direct_sight2((x1, y1), (x2, y2))
      if not direct:
        viewmap[y1][x1].remove( (x2,y2) )



def fill_viewmap(asteroids):
  for x1 in range(width):
    for y1 in range(height):
      if not is_asteroid(x1, y1):
        viewmap[y1][x1] = None
        continue
      viewmap[y1][x1] = list(asteroids)
      fill_viewmap_for_asteroid(x1, y1)



def calc_angle(station, asteroid):
  if station[1] == asteroid[1]:
    if station[0] < asteroid[0]:
      angle = math.pi/2
    else:
      angle = 3*math.pi/2
  elif station[0] == asteroid[0]:
    if station[1] > asteroid[1]:
      angle = 0
    else:
      angle = math.pi
  else:
    if station[0] < asteroid[0] and station[1] > asteroid[1]:
      tangent = abs(float(station[0]-asteroid[0]))/abs(station[1]-asteroid[1])
      angle = math.atan(tangent)
    elif station[0] < asteroid[0] and station[1] < asteroid[1]:
      tangent = abs(float(station[1]-asteroid[1]))/abs(station[0]-asteroid[0])
      angle = math.atan(tangent) + math.pi/2
    elif station[0] > asteroid[0] and station[1] < asteroid[1]:
      tangent = abs(float(station[0]-asteroid[0]))/abs(station[1]-asteroid[1])
      angle = math.atan(tangent) + math.pi
    else:
      tangent = abs(float(station[1]-asteroid[1]))/abs(station[0]-asteroid[0])
      angle = math.atan(tangent) + 3*math.pi/2

  return angle



print_map(asteroidmap)



asteroids = []
for x in range(width):
  for y in range(height):
    if is_asteroid(x, y):
      asteroids += [ (x,y) ]
print "Number of asteroids: %d" % len(asteroids)



viewmap = [ [ None for x in range(width) ] for y in range(height) ]
fill_viewmap(asteroids)
print_viewmap(viewmap)



best = (float('-inf'), None, None)
for x in range(width):
  for y in range(height):
    if viewmap[y][x] is None:
      continue
    if len(viewmap[y][x]) > best[0]:
      best = (len(viewmap[y][x]), x, y)

print "The best location for the monitoring station: %s, detecting %d asteroids" % ((best[1], best[2]), best[0])

asteroidmap[best[2]][best[1]] = 'X'
print_map(asteroidmap)



station = (best[1], best[2])

i = 1
number200 = None
while len(asteroids) > 1:
  asteroids_seen = viewmap[station[1]][station[0]]
  print asteroids_seen

  angles = sorted([ ( a, calc_angle(station, a) ) for a in asteroids_seen], key=lambda e: e[1])
  for a, angle in angles:
    print "The %d. asteroid to be vaporized is at %s" % (i, a)
    asteroidmap[a[1]][a[0]] = '.'
    asteroids.remove(a)
    viewmap[station[1]][station[0]].remove(a)
    if i == 200:
      number200 = (a[0], a[1], 100*a[0] + a[1])
    i += 1
  print_map(asteroidmap)
  fill_viewmap(asteroids)
  print_viewmap(viewmap)


print "The 200th vaporized asteroid's coordinates: (%d,%d) (calculated answer: %d)" % number200
