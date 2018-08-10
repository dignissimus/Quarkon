from Quarkon.logic import *
from Quarkon.utils import circuit


# ~ https://github.com/Qiskit/openqasm/blob/master/examples/generic/adder.qasm

def majority(a, b, c):
    cx(c, b)
    cx(c, a)
    ccx(a, b, c)


def unmaj(a, b, c):
    ccx(a, b, c)
    cx(c, a)
    cx(a, b)


@circuit("Adder")
def adder():
    ans = [0, 0, 0, 0]
