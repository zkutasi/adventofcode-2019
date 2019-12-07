#!/usr/bin/env python

from itertools import permutations
import sys
import time


memory = []
inst_addr = 0

class Mode(object):
  POSITION = '0'
  IMMEDIATE = '1'

class DoSpecific(object):
  HALT = 0



def initialize():
  global memory, inst_addr
  memory = []
  with open(sys.argv[1]) as f:
    for line in f.readlines():
      memory = [ int(i) for i in line.split(',') ]
  inst_addr = 0



def print_state():
  return ','.join( map(lambda i: str(i), memory) )


class Instr(object):
  def __init__(self, inst_addr, params_num, param_modes, io):
    self.params = []
    if params_num > 0:
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
    self.io = io
    

  def do(self):
    print "NOT Implemented instruction"
    sys.exit(1)


class Halt(Instr):
  def __init__(self, inst_addr, modes, io):
    super(Halt, self).__init__(inst_addr, 0, modes, io)

  def do(self):
    return DoSpecific.HALT


class Add(Instr):
  def __init__(self, inst_addr, modes, io):
    super(Add, self).__init__(inst_addr, 3, modes, io)
    
  def do(self):
    args = [None, None]
    memory[self.params[2]] = memory[self.params[0]] + memory[self.params[1]]
    global inst_addr
    inst_addr += len(self.params) + 1
    

class Mult(Instr):
  def __init__(self, inst_addr, modes, io):
    super(Mult, self).__init__(inst_addr, 3, modes, io)

  def do(self):
    memory[self.params[2]] = memory[self.params[0]] * memory[self.params[1]]
    global inst_addr
    inst_addr += len(self.params) + 1


class Input(Instr):
  def __init__(self, inst_addr, modes, io):
    super(Input, self).__init__(inst_addr, 1, modes, io)

  def do(self):
    data = self.io.read()
    memory[self.params[0]] = int(data)
    global inst_addr
    inst_addr += len(self.params) + 1


class Output(Instr):
  def __init__(self, inst_addr, modes, io):
    super(Output, self).__init__(inst_addr, 1, modes, io)

  def do(self):
    self.io.write( memory[self.params[0]] )
    global inst_addr
    inst_addr += len(self.params) + 1


class JumpIfTrue(Instr):
  def __init__(self, inst_addr, modes, io):
    super(JumpIfTrue, self).__init__(inst_addr, 2, modes, io)

  def do(self):
    global inst_addr
    if memory[self.params[0]] != 0:
      inst_addr = memory[self.params[1]]
    else:
      inst_addr += len(self.params) + 1


class JumpIfFalse(Instr):
  def __init__(self, inst_addr, modes, io):
    super(JumpIfFalse, self).__init__(inst_addr, 2, modes, io)

  def do(self):
    global inst_addr
    if memory[self.params[0]] == 0:
      inst_addr = memory[self.params[1]]
    else:
      inst_addr += len(self.params) + 1


class LessThan(Instr):
  def __init__(self, inst_addr, modes, io):
    super(LessThan, self).__init__(inst_addr, 3, modes, io)

  def do(self):
    if memory[self.params[0]] < memory[self.params[1]]:
      memory[self.params[2]] = 1
    else:
      memory[self.params[2]] = 0
    global inst_addr
    inst_addr += len(self.params) + 1


class Equals(Instr):
  def __init__(self, inst_addr, modes, io):
    super(Equals, self).__init__(inst_addr, 3, modes, io)

  def do(self):
    if memory[self.params[0]] == memory[self.params[1]]:
      memory[self.params[2]] = 1
    else:
      memory[self.params[2]] = 0
    global inst_addr
    inst_addr += len(self.params) + 1



class IO(object):
  def __init__(self, inputdata):
    self.inputdata = inputdata
    self.inputptr = 0
    self.outputdata = []
    self.outputptr = -1

  def read(self):
    data = self.inputdata[self.inputptr]
    self.inputptr += 1
    return data

  def write(self, data):
    self.outputdata += [ data ]
    self.outputptr += 1



class InstructionFactory(object):
  def __init__(self):
    self.fact_map = {
       1: Add,
       2: Mult,
       3: Input,
       4: Output,
       5: JumpIfTrue,
       6: JumpIfFalse,
       7: LessThan,
       8: Equals,
      99: Halt
    }
  def get_instruction(self, inst_addr, io):
    param_modes = str(memory[inst_addr] / 100)
    inst = memory[inst_addr] % 100
    instruction = self.fact_map[inst](inst_addr, param_modes, io)
    return instruction



def run_program(phase, rollinginput):
  initialize()
  io = IO([ phase ] + rollinginput)
  while True:
    #print "ip=%d" % inst_addr, memory
    instr = factory.get_instruction(inst_addr, io)
    specifics = instr.do()
    if specifics == DoSpecific.HALT:
      return io.outputdata
    #time.sleep(1)


rollinginput = None
factory = InstructionFactory()
maxthrust = float('-inf')
maxthrust_phase = None
for phases in permutations(range(0,5)):
  rollinginput = [ 0 ]
  for phase in phases:
    rollinginput = run_program(phase, rollinginput)
  print "Ran phase-set %s with result of %d" % (''.join([ str(p) for p in phases ]), rollinginput[0])
  if rollinginput[0] > maxthrust:
    maxthrust = rollinginput[0]
    maxthrust_phase = phases

print "Max thrust available is %d from phase-set %s" % (maxthrust, maxthrust_phase)
