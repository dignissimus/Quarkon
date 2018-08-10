from Quarkon.qubit import Qubit, ClassicalBit


class Register:
    register = []
    size = 0
    regtype = "reg"

    def __getitem__(self, item):
        return self.register[item]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.regtype}[{self.size}] = {self.register}"


class QuantumRegister(Register):
    regtype = "qreg"

    def __init__(self, size):
        self.size = size
        self.register = [Qubit.ZERO() for _ in range(size)]  # initialise with 0


class ClassicalRegister(Register):
    regtype = "creg"

    def __init__(self, size):
        self.size = size
        self.register = [ClassicalBit.ZERO() for _ in range(size)]
