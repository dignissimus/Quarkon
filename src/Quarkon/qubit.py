from decimal import Decimal
from fractions import Fraction
import random
from Quarkon.entanglement import Entanglement


class Qubit:
    @classmethod
    def ZERO(cls):
        return cls(1, 0)

    @classmethod
    def ONE(cls):
        return cls(0, 1)

    def __init__(self, spin_x, spin_y):
        spin_x = Decimal(spin_x)
        spin_y = Decimal(spin_y)
        self.check_spin(spin_x, spin_y)

        self.spin_x = spin_x
        self.spin_y = spin_y

        self.parent_entanglement: Entanglement = None
        self.child_entanglements: [Entanglement] = []

    def debug(self):
        from Quarkon import debug
        debug.debug_object(self)

    @staticmethod
    def from_probability(prob_x, prob_y):
        Qubit.check_probability(prob_x, prob_y)

        spin_x = Decimal(prob_x).sqrt()
        spin_y = Decimal(prob_y).sqrt()

        return Qubit(spin_x, spin_y)

    @staticmethod
    def check_probability(prob_x, prob_y):
        assert prob_x + prob_y == 1

    @staticmethod
    def check_spin(spin_x, spin_y):
        prob_x = Fraction(spin_x ** 2).limit_denominator()
        prob_y = Fraction(spin_y ** 2).limit_denominator()
        Qubit.check_probability(prob_x, prob_y)

    def set_spin_x(self, spin_x):
        prob_x = spin_x ** 2
        assert prob_x <= 1

        spin_y = Decimal(1 - prob_x).sqrt()

        Qubit.check_spin(spin_x, spin_y)

        self.spin_x = spin_x
        self.spin_y = spin_y

    def set_spin_y(self, spin_y):
        prob_y = spin_y ** 2
        assert prob_y <= 1

        spin_x = Decimal(1 - prob_y).sqrt()

        Qubit.check_spin(spin_x, spin_y)

        self.spin_x = spin_x
        self.spin_y = spin_y

    def set_spin(self, spin_x, spin_y):
        Qubit.check_spin(spin_x, spin_y)

        self.spin_x = spin_x
        self.spin_y = spin_y

    def measure(self):
        if self.parent_entanglement:
            self.parent_entanglement.parent.measure()

        prob_x = Fraction(self.spin_x ** 2).limit_denominator()
        prob_y = Fraction(self.spin_y ** 2).limit_denominator()
        Qubit.check_probability(prob_x, prob_y)

        if random.random() <= prob_x:
            self.set_spin_x(Decimal(1))
        else:
            self.set_spin_y(Decimal(1))

        for entanglement in self.child_entanglements:
            child = entanglement.child
            gate = entanglement.gate
            if self.spin_y:
                gate.apply(child)
            child.parent_entanglement = None
        self.child_entanglements = []

        return self


    def collapse(self):
        return int(self.measure().spin_y)

    def copy(self):
        if self.spin_x in [0, 1] and self.spin_y in [0, 1]:
            return Qubit(self.spin_x, self.spin_y)
        raise RuntimeError("Cannot copy a quantum particle")  # TODO: Better error?

    def entangle(self, child, gate):
        entanglement = Entanglement(self, child, gate)
        self.child_entanglements.append(entanglement)
        if child.parent_entanglement:
            child.measure()
        child.parent_entanglement = entanglement

    def __eq__(self, other):
        return self.measure().spin_x == other.measure().spin_x

    def __hash__(self):
        return self.collapse()

    def __repr__(self):
        return str(self.collapse())
