#!/usr/bin/env python

import sys

fuel = 0
with open(sys.argv[1]) as f:
  for line in f.readlines():
    m = int(line)
    f = (m / 3) - 2
    fuel += f

print "Fuel required: %d" % fuel
