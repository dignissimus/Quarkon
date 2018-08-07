from Quarkon.qubit import Qubit

from Quarkon.utils import circuit
from Quarkon.logic import *


@circuit("Entanglement")
def entanglement():
    # I create a qubit and put it into a superposition
    control = Qubit.ZERO()
    qubit = Qubit.ZERO()

    # Has a 50/50 chance of being either a 0 or a 1
    HadamardGate.apply(control)

    # Therefore the qubit has a 50/50 chance of being flipped to a 1
    ControlGate.apply(control, qubit, PauliXGate)

    # The state of the qubit is completely reliant on the control qubit, the two qubits have become entangled
    # Right now, if the control qubit is a 0, the qubit stays the same and is also a 0
    # If the control qubit, however, was a 1, the qubit would flip and become a 1 too
    # This means that the qubits, no matter the outcome will be the same
    # Also, we have a 50/50 chance of the qubits being either |00> and |11> (|00> + |11> / sqrt(2))
    # I can make them hold different values before they have collapsed by applying the Pauli-X gate on one qubit
    PauliXGate.apply(qubit)

    return control, qubit


entanglement(repeat=1000)
