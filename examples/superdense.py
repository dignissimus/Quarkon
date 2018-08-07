from Quarkon.qubit import Qubit
from Quarkon.utils import circuit

ONE = Qubit.from_probability(0, 1)
ZERO = Qubit.from_probability(1, 0)


@circuit("Superdense Encoding")
def encoding_test(bit0, bit1):
    # First create superposition (|00> + |11>) /  sqrt(2)
    # This means we have a 50% chance of getting 0, 0 and a 50% chance of 1, 1
    # And these are the only possible combinations

    # I do this, by getting the Hadamard on my control qubit and using this to
    # determine the state of the first superposition qubit
    # I use this state to control the state of the next qubit, if the bit is changed, I flip
    # the second bit, if not they both stay as 0
    pass


encoding_test(0, 1)
