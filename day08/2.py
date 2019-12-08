#!/usr/bin/env python

import sys
from collections import Counter


data = None
with open(sys.argv[1]) as f:
  for line in f.readlines():
    data = line.strip()


w = int(sys.argv[2])
h = int(sys.argv[3])


layers = []
layersize = w*h
i = 0
while i < len(data):
  layers += [ data[i:i+layersize] ]
  i += (w*h)


print "Layers:"
for l in range(len(layers)):
  print "%2d: %s" % (l, layers[l])


counters = [ Counter(l) for l in layers ]
print "Number of layers: %d" % len(layers)

image = [ [ 'x' for y in range(h) ] for x in range(w) ]

for layer in layers[::-1]:
  for i in range(w):
    for j in range(h):
      if layer[j*w+i] == '0':
        image[i][j] = ' '
      elif layer[j*w+i] == '1':
        image[i][j] = '#'
      elif layer[j*w+i] == '2':
        pass


print "Image:"
print "   %s" % ''.join([ str(n/10 if n >= 10 else ' ') for n in range(w) ])
print "   %s" % ''.join([ str(n % 10) for n in range(w) ])
print
for y in range(h):
  print "%2d %s" % (y, ''.join([ image[x][y] for x in range(w) ]))
