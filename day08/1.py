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
print "Layer stats: %s" % counters
minzeros = float('inf')
mincounter = None
for c in counters:
  print "Number of Zeroes: %d, Ones multiplied by Twos: %d" % (c['0'], c['1']*c['2'])
  if c['0'] < minzeros:
    minzeros = c['0']
    mincounter = c['1']*c['2']

print "Answer: %d" % mincounter
