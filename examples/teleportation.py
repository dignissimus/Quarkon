from Quarkon.utils import circuit
from Quarkon.logic import *


@circuit("Teleportation")
def teleportation_circuit():
    HadamardGate.apply(q[1])
    cx(q[1], q[2])
    cx(q[0], q[1])
    HadamardGate.apply(q[0])
    q[0].collapse() # In this scenario .measure is fine as well
    q[1].collapse()
  
    cx(q[1], q[2])
    cz(q[0], q[2])
  
    return q

teleportation_cirquit(1, 0, 1)
