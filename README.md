# Quarkon
Quarkon simulates Quantum circuits which may be written in Python or QASM.

Quarkon also provides an implementation of [Qasm 2.0](https://github.com/Qiskit/openqasm/blob/master/spec/qasm2.rst)

## Creating a circuit in Python
In Python, to create a circuit, you may use the the `@circuit` decorator found in `Quarkon.utils`, you may optionally give your circuit a name by supplying a string as a parameter to the decorator.
Logic gates are found in `Quarkon.logic` and the Qubit is found in `Quarkon.qubit` and you may apply them on a qubit by using `LogicGate.apply(qubit)` where `LogicGate` is your desired logic gate. Yout circuit function may optionally take its input qubits as separate parameters or take them all in one tuple.

## Creating a circuit in QASM
QASM is very much like most assembly languages. 

The first uncommented line of your `.qasm` file must be `OPENQASM 2.0;`, all subsequent lines may be anything ranging from gate definitions to register declarations.

To apply a gate on a bit you type the mnemonic for the gate followed by the bits you want to be arguments for that gate, the statement is then terminated with a semicolon.
To apply the hadamard gate on a qubit you qould write
```asm
h qubit;
```
QASM makes use of registers, registers are automatically initialised so that each bit has the value of 0, you may have classical and Quantum registers, to define a quantum register, you write `qreg NAME[CAPACITY]` where `NAME` is the name of the register and `CAPACITY` is how many qubits it can hold. You can substitute `qreg` for `creg` in order to declare a classical register which instead holds classical bits.
```asm
qreg qreg1[5];
qreg qreg2[5];
creg output[5]
x qreg1; // applies the Pauli-X gate to every Qubit in qreg1
x qreg1[0]; // applies the Pauli-X gate to the first Qubit in qreg 1
cx qreg1 qreg2; // Equivalent to cx qreg1[0] qreg2[0]; qreg1[1] qreg2[1]... 
measure qreg2 -> output; // equivalent to measure qreg2[0] output[0] qreg2[1] output[1]...
```

To define a gate you write `gate` followed by the name of the gate then the arguments of that gate, a gate that takes two qubits and 'entangles' them for a certain configuration might look something similar to
```asm
gate entangle a, b {
    h a;
    cx a b;
    x b;
}

qreg qreg1[5];
qreg qreg2[5];

// At the end of the programme, the qubits inside the quantum registers collapse to a state of either 1 or 0 and are displayed in the terminal

```

## Examples
### Creating an EPR pair
```python
@circuit("EPR Pair")
def epr_pair(q):
  h(q[0]) # = HadamardGate.apply(q[0])
  cx(q[0], q[1]) # = ControlGate.apply(q[0], q[1], PauliXGate)
  return q

epr_pair(0, 0)
```
Equivalent qasm 
```asm
qreg	q[2];

h	q[0];
cnot	q[0], q[1];
```

### Teleportation circuit
```python
@circuit("Teleportation")
def teleportation_circuit(q):
  h(q[1])
  cx(q[1], q[2])
  cx(q[0], q[1])
  h(q[0])

  q[0].collapse() # In this scenario .measure is fine too
  q[1].collapse()
  
  cx(q[1], q[2])
  cz(q[0], q[2])
  
  return q
```
Equivalent qasm
```asm
qreg	q[3];

h	q[1];
cnot	q[1], q[2];
cnot	q[0], q[1];
h	q[0];
measure	q[0] -> q[0];
measure	q[1] -> q[1];
cx	q[1], q[2];
cz	q[0], q[2];
```
