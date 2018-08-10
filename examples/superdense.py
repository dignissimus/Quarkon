from Quarkon.logic import *
from Quarkon.utils import circuit

ONE = Qubit.from_probability(0, 1)
ZERO = Qubit.from_probability(1, 0)


@circuit("Superdense Encoding")
def encoding_test(bit0, bit1):  # TODO:  Doesn't work, I don't know why maybe Z gate implemented incorrectly
    # First create superposition (|00> + |11>) /  sqrt(2)
    # This means we have a 50% chance of getting 0, 0 and a 50% chance of 1, 1
    # And these are the only possible combinations
    # I do this, by getting the Hadamard on my control qubit and using this to
    # determine the state of the first superposition qubit
    # I use this state to control the state of the next qubit, if the bit is changed, I flip
    # the second bit, if not they both stay as 0

    control = h(Qubit.ZERO())
    alice_qubit = Qubit.ZERO()
    bob_qubit = Qubit.ZERO()

    cx(control, alice_qubit)
    cx(alice_qubit, bob_qubit)

    # If the first bit is 1, we flip alice's qubit
    # If the second bit is 1, we alter the phase of bob's qubit
    cx(bit0, alice_qubit)
    cz(bit1, alice_qubit)

    # Bob's side
    cx(alice_qubit, bob_qubit)
    bit0 = bob_qubit.collapse()
    h(alice_qubit)
    bit1 = alice_qubit.collapse()
    return bit0, bit1


encoding_test(0, 1)
