#!/usr/bin/env python

from collections import defaultdict
from Queue import Queue
import random
import sys
import time



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


class HullIO(object):
  def __init__(self):
    self.curr_pos = (0,0)
    self.history = {}
    self.history[ self.curr_pos ] = 1
    self.inputqueue = Queue()
    self.outputqueue = None
    self.robot_facing = '^'
    self.is_data_for_color = True

  def read(self):
    if self.curr_pos not in self.history:
      return 0
    else:
      return self.history[self.curr_pos]

  def write(self, data):
    if self.is_data_for_color:
      self.history[self.curr_pos] = data
    else:
      if data == 0:
        if self.robot_facing == '^':
          self.robot_facing = '<'
          newpos = ( self.curr_pos[0]-1, self.curr_pos[1] )
        elif self.robot_facing == '<':
          self.robot_facing = 'v'
          newpos = ( self.curr_pos[0], self.curr_pos[1]+1 )
        elif self.robot_facing == 'v':
          self.robot_facing = '>'
          newpos = ( self.curr_pos[0]+1, self.curr_pos[1] )
        else:
          self.robot_facing = '^'
          newpos = ( self.curr_pos[0], self.curr_pos[1]-1 )
      else:
        if self.robot_facing == '^':
          self.robot_facing = '>'
          newpos = ( self.curr_pos[0]+1, self.curr_pos[1] )
        elif self.robot_facing == '<':
          self.robot_facing = '^'
          newpos = ( self.curr_pos[0], self.curr_pos[1]-1 )
        elif self.robot_facing == 'v':
          self.robot_facing = '<'
          newpos = ( self.curr_pos[0]-1, self.curr_pos[1] )
        else:
          self.robot_facing = 'v'
          newpos = ( self.curr_pos[0], self.curr_pos[1]+1 )

      self.curr_pos = newpos
      self.print_hull()
      self.print_history_data()

    self.is_data_for_color = not self.is_data_for_color

  def print_hull(self):
    minx = min([ pos[0] for pos in self.history ])
    maxx = max([ pos[0] for pos in self.history ])
    width = maxx - minx + 1
    miny = min([ pos[1] for pos in self.history ])
    maxy = max([ pos[1] for pos in self.history ])
    height = maxy - miny + 1

    hull = [ [ 0 for x in range(width) ] for y in range(height) ]
    for y in range(height):
      for x in range(width):
        historydata = [ color for pos, color in self.history.items() if pos == (x+minx, y+miny) ]
        hull[y][x] = historydata[-1] if len(historydata) > 0 else 0

    for y in range(height):
      print ''.join([ '.' if e == 0 else '#' for e in hull[y] ])
    print

  def print_history_data(self):
    print "Panels painted so far: %d" % len(self.history)


class ArcadeIO(object):
  def __init__(self, computer):
    self.computer = computer
    self.steps = 0
    self.arcade = defaultdict(lambda: ' ')
    self.data_type = 0
    self.pos = []
    self.score = 0
    self.ball_touched_bottom = False
    self.ball_pos = None
    self.ball_dir = None
    self.ball_bottom_pos = None
    self.current_paddle_position = None

  def read(self):
    if self.ball_pos[1] == self.current_paddle_position[1]-1:
      if self.ball_pos[0] == self.current_paddle_position[0]:
        if self.steps > 1000:
          return random.choice([ self.ball_dir, 0 ])
        else:
          return self.ball_dir
      else:
        return self.ball_dir

    simulation = Computer()
    for k,v in self.computer.memory.items():
      simulation.memory[k] = v
    simulation.inst_addr = self.computer.inst_addr
    simulation.relative_base = self.computer.relative_base
    for k,v in self.computer.io.arcade.items():
      simulation.io.arcade[k] = v
    simulation.io.ball_pos = self.ball_pos
    simulation.io.ball_dir = self.ball_dir
    simulation.io.ball_bottom_pos = self.ball_bottom_pos
    simulation.io.current_paddle_position = self.current_paddle_position
    simulation.io.read = lambda: -1
    simulation.io.print_arcade = lambda: None
    simulation.run_program()
    expected_landing_spot = simulation.io.ball_bottom_pos[0]

    print "Expected to land on %d" % expected_landing_spot
    return expected_landing_spot - self.current_paddle_position[0]

  def simulate_ball_bottom(self):
    if not self.ball_touched_bottom and self.current_paddle_position and self.pos[1] == self.current_paddle_position[1]-1:
      self.ball_bottom_pos = tuple(self.pos)
      self.ball_touched_bottom = True

  def write(self, data):
    if self.data_type in [0,1]:
      self.pos += [ data ]
      self.data_type += 1
    else:
      if self.pos == [-1, 0]:
        self.score = data
      else:
        ch = ' '
        if data == 1:
          ch = '#'
        elif data == 2:
          ch = '*'
        elif data == 3:
          ch = '-'
          self.current_paddle_position = self.pos
        elif data == 4:
          ch = 'O'
          if self.ball_pos:
            if self.ball_pos[0] > self.pos[0]:
              self.ball_dir = -1
            else:
              self.ball_dir = 1
          self.ball_pos = tuple(self.pos)
          self.simulate_ball_bottom()
          self.steps += 1
        self.arcade[ tuple(self.pos) ] = ch
        if ch == 'O':
          self.print_arcade()
      self.pos = []
      self.data_type = 0

  def print_arcade(self):
    minx = min([ x for x,y in self.arcade.keys() ])
    maxx = max([ x for x,y in self.arcade.keys() ])
    miny = min([ y for x,y in self.arcade.keys() ])
    maxy = max([ y for x,y in self.arcade.keys() ])
    width = maxx - minx + 1
    height = maxy - miny + 1
    print "   %s    steps: %d, score: %d" % ( ''.join([ str(i/10) if i>9 else ' ' for i in range(width) ]), self.steps, self.score)
    print "   %s" % ''.join([ str(i%10) for i in range(width) ])
    for j in range(height):
      row = [ ' ' for x in range(width) ]
      for i in range(width):
        row[i] = self.arcade[ (i,j) ]
      print "%2d %s" % (j, ''.join(row) )
    print
    #time.sleep(1)



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
    self.io = ArcadeIO(self)
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
arcade = Computer()
arcade.memory[0] = 2

arcade.run_program()
print "The final score is: %d" % arcade.io.score
