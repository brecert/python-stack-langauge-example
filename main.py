import sys
from enum import Enum

class InstructionType(Enum):
    NUM = 0
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4
    DEO = 126
    DBG = 127
    END = 128

# todo: research more and see if this is already std
def try_float(n):
  try:
    return float(n)
  except ValueError:
    return None

def parse(str):
  stack = [InstructionType.END]

  for atom in str.split():
    atom = atom.lstrip('(').rstrip(')')
    match atom:
      case "(": continue
      case ")": continue
      case "+": stack.append(InstructionType.ADD)
      case "-": stack.append(InstructionType.SUB)
      case "*": stack.append(InstructionType.MUL)
      case "/": stack.append(InstructionType.DIV)
      case _ if atom in InstructionType.__members__:
        stack.append(InstructionType[atom])
      case _ if (num := try_float(atom)) is not None:
        stack.append(num)
      case _:
        raise Exception(f"Unknown atom: {atom}")

  return stack

def run(stack):
  while True:
    match stack:
      case [*stack, a, InstructionType.ADD, b]:
        stack.append(a + b)
      case [*stack, a, InstructionType.SUB, b]:
        stack.append(a - b)
      case [*stack, a, InstructionType.MUL, b]:
        stack.append(a * b)
      case [*stack, a, InstructionType.DIV, b]:
        stack.append(a / b)
      case [*stack, InstructionType.END]:
        break
      case [*stack, InstructionType.DEO, a]:
        print(a)
      case [*stack, InstructionType.DBG]:
        print(stack[-1])
      case []:
        raise Exception("Stack underflow")
      case _:
        raise Exception(f"No match for instruction in stack: {stack}")

if __name__ == "__main__":
  stack = parse(" ".join(sys.argv[1:]))
  run(stack)