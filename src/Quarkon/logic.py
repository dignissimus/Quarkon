from Quarkon.qubit import Qubit
from Quarkon.utils import abstract
from decimal import Decimal


class Gate:
    @staticmethod
    @abstract
    def apply(qubit: Qubit) -> Qubit:
        return qubit


class HadamardGate(Gate):  # (A + B) / sqrt(2), (A - B) / sqrt(2)
    @staticmethod
    def apply(qubit: Qubit) -> Qubit:
        new_spin_x = Decimal(qubit.spin_x + qubit.spin_y) / Decimal(2).sqrt()
        new_spin_y = Decimal(qubit.spin_x - qubit.spin_y) / Decimal(2).sqrt()

        qubit.set_spin(new_spin_x, new_spin_y)
        return qubit


class QuantumNotGate(Gate):  # Pauli-X
    @staticmethod
    def apply(qubit: Qubit) -> Qubit:
        new_spin_x = qubit.spin_y
        new_spin_y = qubit.spin_x

        qubit.set_spin(new_spin_x, new_spin_y)
        return qubit


PauliXGate = QuantumNotGate


class PauliZGate(Gate):  # TODO: correct?
    @staticmethod
    def apply(qubit: Qubit):
        new_spin_y = -qubit.spin_y
        qubit.set_spin_y(new_spin_y)


class ControlGate:
    @staticmethod
    def apply(control: Qubit, qubit: Qubit, gate):
        if control.spin_x in [0, 1] and not control.parent_entanglement:
            if control.collapse():
                gate.apply(qubit)
        else:
            control.entangle(qubit, gate)


def cnot(control: Qubit, qubit: Qubit):
    ControlGate.apply(control, qubit, PauliXGate)


def ccnot(control: Qubit, control2: Qubit, qubit: Qubit):
    # def ccnot a, b, c {
    #  {
    #    d = not b
    #    cnot a, d
    #  }
    #   cnot d, c
    # }

    d = Qubit.ONE()
    # We need it so that qubit d is the opposite of b (control2), the cnot gate works for this
    cnot(control2, d)

    cnot(control, d)
    cnot(d, qubit)


def cz(control: Qubit, qubit: Qubit):
    ControlGate.apply(control, qubit, PauliZGate)


def ch(control: Qubit, qubit: Qubit):
    ControlGate.apply(control, qubit, HadamardGate)


h = HadamardGate.apply
cx = cnot
ccx = ccnot
x = PauliXGate.apply
z = PauliZGate.apply