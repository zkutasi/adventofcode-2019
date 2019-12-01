#!/usr/bin/env python

import sys
import time

fuel = 0


def fuel_for_mass(mass):
  return (mass / 3) - 2


with open(sys.argv[1]) as f:
  for line in f.readlines():
    m = int(line)

    fuel4mass = fuel_for_mass(m)
    fuel += fuel4mass
    while fuel4mass > 0:
      m2 = fuel_for_mass(fuel4mass)
      if m2 > 0:
        fuel += m2
      fuel4mass = m2

print "Fuel required (fuel itself calculated in): %d" % fuel
