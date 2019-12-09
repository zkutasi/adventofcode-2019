#!/usr/bin/env python

from collections import defaultdict
from Queue import Queue
import sys


class Mode(object):
  POSITION = '0'
  IMMEDIATE = '1'
  RELATIVE = '2'

class DoSpecific(object):
  HALT = 0






class Instr(object):
  def __init__(self, computer, params_num, param_modes):
    self.computer = computer
    self.params = []
    self.param_modes = []
    if params_num > 0:
      self.param_modes = [ Mode.POSITION for m in range(params_num) ]
      for p in range(len(param_modes)):
        self.param_modes[p] = param_modes[len(param_modes)-p-1]
    for p in range(params_num):
      if self.param_modes[p] == Mode.POSITION:
        self.params += [ self.computer.memory[self.computer.inst_addr+p+1] ]
      elif self.param_modes[p] == Mode.IMMEDIATE:
        self.params += [ self.computer.inst_addr+p+1 ]
      elif self.param_modes[p] == Mode.RELATIVE:
        self.params += [ self.computer.memory[self.computer.inst_addr+p+1 ] + self.computer.relative_base ]
      else:
        print "NOT Implemented Mode: %s" % self.param_modes[p]
        sys.exit(1)
    #print "DEBUG:", "instr_addr", self.computer.inst_addr, "Instr:", self.__class__, "modes:", self.param_modes, "param addresses:", self.params, "params:", [ self.computer.memory[p] for p in self.params ]
    

  def do(self):
    print "NOT Implemented instruction"
    sys.exit(1)


class Halt(Instr):
  def __init__(self, computer, modes):
    super(Halt, self).__init__(computer, 0, modes)

  def do(self):
    return DoSpecific.HALT


class Add(Instr):
  def __init__(self, computer, modes):
    super(Add, self).__init__(computer, 3, modes)
    
  def do(self):
    args = [None, None]
    self.computer.memory[self.params[2]] = self.computer.memory[self.params[0]] + self.computer.memory[self.params[1]]
    self.computer.inst_addr += len(self.params) + 1
    

class Mult(Instr):
  def __init__(self, computer, modes):
    super(Mult, self).__init__(computer, 3, modes)

  def do(self):
    self.computer.memory[self.params[2]] = self.computer.memory[self.params[0]] * self.computer.memory[self.params[1]]
    self.computer.inst_addr += len(self.params) + 1


class Input(Instr):
  def __init__(self, computer, modes):
    super(Input, self).__init__(computer, 1, modes)

  def do(self):
    data = self.computer.io.read()
    self.computer.memory[self.params[0]] = int(data)
    self.computer.inst_addr += len(self.params) + 1


class Output(Instr):
  def __init__(self, computer, modes):
    super(Output, self).__init__(computer, 1, modes)

  def do(self):
    self.computer.io.write( self.computer.memory[self.params[0]] )
    self.computer.inst_addr += len(self.params) + 1


class JumpIfTrue(Instr):
  def __init__(self, computer, modes):
    super(JumpIfTrue, self).__init__(computer, 2, modes)

  def do(self):
    if self.computer.memory[self.params[0]] != 0:
      self.computer.inst_addr = self.computer.memory[self.params[1]]
    else:
      self.computer.inst_addr += len(self.params) + 1


class JumpIfFalse(Instr):
  def __init__(self, computer, modes):
    super(JumpIfFalse, self).__init__(computer, 2, modes)

  def do(self):
    if self.computer.memory[self.params[0]] == 0:
      self.computer.inst_addr = self.computer.memory[self.params[1]]
    else:
      self.computer.inst_addr += len(self.params) + 1


class LessThan(Instr):
  def __init__(self, computer, modes):
    super(LessThan, self).__init__(computer, 3, modes)

  def do(self):
    if self.computer.memory[self.params[0]] < self.computer.memory[self.params[1]]:
      self.computer.memory[self.params[2]] = 1
    else:
      self.computer.memory[self.params[2]] = 0
    self.computer.inst_addr += len(self.params) + 1


class Equals(Instr):
  def __init__(self, computer, modes):
    super(Equals, self).__init__(computer, 3, modes)

  def do(self):
    if self.computer.memory[self.params[0]] == self.computer.memory[self.params[1]]:
      self.computer.memory[self.params[2]] = 1
    else:
      self.computer.memory[self.params[2]] = 0
    self.computer.inst_addr += len(self.params) + 1


class RelativeBaseOffset(Instr):
  def __init__(self, computer, modes):
    super(RelativeBaseOffset, self).__init__(computer, 1, modes)

  def do(self):
    self.computer.relative_base += self.computer.memory[self.params[0]]
    self.computer.inst_addr += len(self.params) + 1



class BasicIO(object):
  def __init__(self):
    pass

  def read(self):
    data = raw_input("Input: ")
    return int(data)

  def write(self, data):
    print data


class QueueIO(object):
  def __init__(self):
    self.inputqueue = Queue()
    self.outputqueue = None

  def read(self):
    return self.inputqueue.get()

  def write(self, data):
    self.outputqueue.put(data)


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
       9: RelativeBaseOffset,
      99: Halt
    }
  def get_instruction(self, computer):
    param_modes = str(computer.memory[computer.inst_addr] / 100)
    inst = computer.memory[computer.inst_addr] % 100
    instruction = self.fact_map[inst](computer, param_modes)
    return instruction


class Computer(object):
  def __init__(self):
    self.io = BasicIO()
    self.memory = defaultdict(lambda: 0)
    self.inst_addr = 0
    self.relative_base = 0
    with open(sys.argv[1]) as f:
      for line in f.readlines():
        prog = [ int(i) for i in line.split(',') ]
        for m in range(len(prog)):
          self.memory[m] = prog[m]

  def run_program(self):
    while True:
      instr = factory.get_instruction(self)
      specifics = instr.do()
      if specifics == DoSpecific.HALT:
        return



factory = InstructionFactory()
c = Computer()
c.run_program()





