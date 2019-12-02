#!/usr/bin/env python

import sys

program = []
with open(sys.argv[1]) as f:
  for line in f.readlines():
    program = [ int(i) for i in line.split(',') ]



def print_state():
  return ','.join( map(lambda i: str(i), program) )



program[1] = 12
program[2] = 2
op = 0
print "Starting state at op=%d is: %s" % (op, print_state())
while program[op] != 99:
  if program[op] == 1:
    program[program[op+3]] = program[program[op+1]] + program[program[op+2]]
  elif program[op] == 2:
    program[program[op+3]] = program[program[op+1]] * program[program[op+2]]
  else:
    print "ERROR"
    exit(1)
  print "Intermediate state at op=%d is: %s" % (op, print_state())
  op += 4

print "The final state is: %s" % print_state()
