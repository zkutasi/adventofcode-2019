#!/usr/bin/env python

import sys

memory = []
inst_addr = 0

class Mode(object):
  POSITION = '0'
  IMMEDIATE = '1'

class DoSpecific(object):
  HALT = 0


def initialize():
  global memory, inst_addr
  with open(sys.argv[1]) as f:
    for line in f.readlines():
      memory = [ int(i) for i in line.split(',') ]
  inst_addr = 0



def print_state():
  return ','.join( map(lambda i: str(i), memory) )


class Instr(object):
  def __init__(self, inst_addr, params_num=0, param_modes=''):
    self.params = []
    self.param_modes = [ Mode.POSITION for m in range(params_num) ]
    for p in range(len(param_modes)):
      self.param_modes[p] = param_modes[len(param_modes)-p-1]
    for p in range(params_num):
      if self.param_modes[p] == Mode.POSITION:
        self.params += [ memory[inst_addr+p+1] ]
      elif self.param_modes[p] == Mode.IMMEDIATE:
        self.params += [ inst_addr+p+1 ]
      else:
        print "NOT Implemented Mode: %s" % self.param_modes[p]
        sys.exit(1)
    

  def do(self):
    print "NOT Implemented instruction"
    sys.exit(1)

  def post_do(self):
    global inst_addr
    inst_addr += len(self.params) + 1


class Halt(Instr):
  def __init__(self, inst_addr, modes):
    super(Halt, self).__init__(inst_addr)

  def do(self):
    return DoSpecific.HALT


class Add(Instr):
  def __init__(self, inst_addr, modes):
    super(Add, self).__init__(inst_addr, 3, modes)
    
  def do(self):
    args = [None, None]
    memory[self.params[2]] = memory[self.params[0]] + memory[self.params[1]]
    

class Mult(Instr):
  def __init__(self, inst_addr, modes):
    super(Mult, self).__init__(inst_addr, 3, modes)

  def do(self):
    memory[self.params[2]] = memory[self.params[0]] * memory[self.params[1]]


class Input(Instr):
  def __init__(self, inst_addr, modes):
    super(Input, self).__init__(inst_addr, 1, modes)

  def do(self):
    data = raw_input("Input: ")
    memory[self.params[0]] = int(data)


class Output(Instr):
  def __init__(self, inst_addr, modes):
    super(Output, self).__init__(inst_addr, 1, modes)

  def do(self):
    print memory[self.params[0]]


class InstructionFactory(object):
  def __init__(self):
    self.fact_map = {
       1: Add,
       2: Mult,
       3: Input,
       4: Output,
      99: Halt
    }
  def get_instruction(self, inst_addr):
    param_modes = str(memory[inst_addr] / 100)
    inst = memory[inst_addr] % 100
    instruction = self.fact_map[inst](inst_addr, param_modes)
    return instruction



def run_program():
  initialize()
  while True:
    
    instr = factory.get_instruction(inst_addr)
    specifics = instr.do()
    if specifics == DoSpecific.HALT:
      return memory[0]
    instr.post_do()


factory = InstructionFactory()
run_program()
