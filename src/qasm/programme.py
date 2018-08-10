from Quarkon.logic import *
from Quarkon.qubit import Bit
from pprint import pprint
from qasm.register import Register


class RegisterSlice:
    def __init__(self, register_name, offset):
        self.register_name = register_name
        self.offset = offset


class NamedValue:
    def __init__(self, name):
        self.name = name


class VersionStatement:
    def __init__(self, version_string):
        self.version_string = version_string
        m = version_string.split(".")
        self.major = int(m[0])
        self.minor = int(m[1])


class IncludeStatement:
    def __init__(self, file):
        self.file = file


class Operation:
    def __init__(self, operation, args):
        self.operation = operation
        self.args = args


class GateDeclaration:
    def __init__(self, name, params, operations):
        self.name = name
        self.params = params
        self.operations = operations


class RegisterDeclaration:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class QuantumRegisterDeclaration(RegisterDeclaration):
    pass


class ClassicalRegisterDeclaration(RegisterDeclaration):
    pass


class GateDefinition:
    def __init__(self, name, params, operations):
        self.name = name
        self.params = params
        self.operations = operations


class Measurement:
    def __init__(self, from_location, to_location):
        self.from_location = from_location
        self.to_location = to_location


class Programme:
    @staticmethod
    def measure_into(qubit, classical_bit):
        classical_bit.value = qubit.collapse()

    operators = {
        "h": h,  # Hadamard Gate
        "ch": ch,  # Controlled  Hadamard Gate
        "cnot": cnot,  # Controlled Not Gate
        "x": x,  # Pauli-X Gate
        "cx": cx,  # Controlled Pauli-X gate
        "z": z,  # Pauli-Z Gate
        "ccx": ccx,  # Controlled Controlled Pauli-X Gate (Toffoli Gate)
        "measure": measure_into
    }

    def __init__(self, version=None, includes=[], operations=[]):
        self.classical_registers = {}
        self.gates = {}
        self.quantum_registers = {}
        self.version = version
        self.includes = includes
        self.operations = operations

    def execute(self):
        for name, gate in self.gates.items():
            self.define_gate(name, gate)

        all_registers = {**self.quantum_registers, **self.classical_registers}
        for operation in self.operations:
            self.perform_operation(operation, all_registers)

        print("Outputting Register contents")
        pprint(all_registers)

    def define_gate(self, name, gate):
        def gate_function(*args):
            local_scope = {}
            for param, arg in zip(gate.params, args):
                local_scope[param] = arg
            for operation in gate.operations:
                self.perform_operation(operation, local_scope)

        self.operators[name] = gate_function

    def perform_operation(self, operation, scope):
        to_execute = None
        arguments = []

        if type(operation) == Operation:
            arguments = operation.args
            to_execute = self.operators[operation.operation]
        elif type(operation) == Measurement:
            arguments = [operation.from_location, operation.to_location]
            to_execute = Programme.measure_into
        else:
            print(f"Unknown operation {operation}, exiting..")
            exit()
        if len(set([type(arg) for arg in arguments])) != 1:  # TODO: Implement
            print("TODO: Better 'loop' args")
            exit()

        if type(arguments[0]) == RegisterSlice:  # They're all register slices
            new_arguments = []
            for regslice in arguments:
                new_arguments.append(scope[regslice.register_name][regslice.offset])
            to_execute(*new_arguments)

        elif type(arguments[0] == NamedValue):
            arguments = [scope[arguments.name] for arguments in arguments]
            test = arguments[0]
            if isinstance(test, Register):
                registers = arguments
                for i in range(registers[0].size):
                    to_execute(*[register[i] for register in registers])
            elif isinstance(test, Bit):
                to_execute(*arguments)
