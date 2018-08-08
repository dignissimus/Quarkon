# Quarkon
Quantum circuit simulation in python

## Creating a circuit
To create a circuit, you may use the the `@circuit` decorator found in `Quarkon.utils`, you may optionally give your circuit a name by supplying a string as a parameter to the decorator.
Logic gates are found in `Quarkon.logic` and the Qubit is found in `Quarkon.qubit` and you may apply them on a qubit by using `LogicGat.apply(qubit)` where `LogicGate` is your desired logic gate. Yout circuit function may optionally take its input qubits as separate parameters or take them all in one tuple.
## Examples
### Creating an EPR pair
```python
from Quarkon.logic import * 
@circuit("EPR Pair")
def epr_pair(q):
  HadamardGate.apply(q[0])
  cx(q[0], q[1]) # = ControlGate.apply(q[0], q[1], PauliXGate)
  return q

epr_pair(0, 0)
```
Equivalent qasm 
```asm
qubit 	q0
qubit 	q1

h	q0
cnot	q0,q1
```

### Teleportation circuit
```python
@circuit("Teleportation")
def teleportation_circuit():
  HadamardGate.apply(q[1])
  cx(q[1], q[2])
  cx(q[0], q[1])
  HadamardGate.apply(q[0])
  q[0].collapse() # In this scenario .measure is fine as well
  q[1].collapse()
  
  cx(q[1], q[2])
  cx(q[0], q[2])
  
  return q
```
Equivalent qasm
```asm
qubit 	q0
qubit 	q1
qubit 	q2

h	q1
cnot	q1,q2
cnot	q0,q1
h	q0
nop	q1
measure	q0	
measure	q1
c-x	q1,q2
c-z	q0,q2
```
