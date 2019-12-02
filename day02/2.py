#!/usr/bin/env python

import sys

memory = []
inst_addr = 0

def initialize():
  global memory, inst_addr
  with open(sys.argv[1]) as f:
    for line in f.readlines():
      memory = [ int(i) for i in line.split(',') ]
  inst_addr = 0



def print_state():
  return ','.join( map(lambda i: str(i), memory) )


class Instr(object):
  def __init__(self, inst_addr, params_num):
    self.params = memory[inst_addr+1:inst_addr+params_num+1]

  def do(self):
    print "NOT Implemented instruction"
    sys.exit(1)


class Halt(Instr):
  def __init__(self, inst_addr):
    super(Halt, self).__init__(inst_addr, 0)

  def do(self):
    return True


class Add(Instr):
  def __init__(self, inst_addr):
    super(Add, self).__init__(inst_addr, 3)
    
  def do(self):
    global inst_addr
    memory[self.params[2]] = memory[self.params[0]] + memory[self.params[1]]
    inst_addr += len(self.params) + 1
    return False
    

class Mult(Instr):
  def __init__(self, inst_addr):
    super(Mult, self).__init__(inst_addr, 3)

  def do(self):
    global inst_addr
    memory[self.params[2]] = memory[self.params[0]] * memory[self.params[1]]
    inst_addr += len(self.params) + 1
    return False


class InstructionFactory(object):
  def __init__(self):
    self.fact_map = {
       1: Add,
       2: Mult,
      99: Halt
    }
  def get_instruction(self, inst_addr):
    inst = memory[inst_addr]
    instruction = self.fact_map[inst](inst_addr)
    return instruction



def run_program(noun, verb):
  initialize()
  memory[1] = noun
  memory[2] = verb
  while True:
    do_break = factory.get_instruction(inst_addr).do()
    if do_break:
      return memory[0]


factory = InstructionFactory()
#lookingfor = 12490719
lookingfor = 19690720
for noun in range(100):
  for verb in range(100):
    res = run_program(noun, verb)
    if res == lookingfor:
      print "output=%d found with noun=%d and verb=%d, 100 * noun + verb = %d" % (lookingfor, noun, verb, 100 * noun + verb)
      sys.exit(0)
