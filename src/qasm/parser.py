from qasm.register import QuantumRegister, ClassicalRegister
from qasm.programme import *

OPENQASM = "OPENQASM"
SEMICOLON = ";"
INCLUDE = "include"
GATE = "gate"
QREG = "qreg"
CREG = "creg"
MEASURE = "measure"
ARROW = "->"


class Parser:
    def __init__(self, tokens: [str]):
        while "" in tokens:
            tokens.remove("")
        self.tokens = tokens
        self.programme = Programme()
        self.index = 0
        self.parsed = []
        self.parse()

    def read_token(self):
        try:
            token = self.tokens[self.index]
            self.index += 1
            return token
        except IndexError:
            return None

    def skip_token(self):
        self.read_token()

    def peek_token(self):
        try:
            return self.tokens[self.index]
        except IndexError:
            return None

    def read_version(self):
        assert self.read_token() == OPENQASM
        version_string = self.read_token()
        semicolon = self.read_token()
        assert semicolon == SEMICOLON
        version = VersionStatement(version_string)
        self.programme.version = version
        self.parsed.append(version)

    def read_include(self):
        assert self.read_token() == INCLUDE
        file = self.read_string()
        assert self.read_token() == ";"
        include = IncludeStatement(file)
        self.parsed.append(include)
        self.programme.includes.append(include)

    def read_string(self):
        string = self.read_token()
        return string

    def read_name(self):
        name = self.read_token()
        return name

    def read_operation(self, global_scope=False):
        op = self.read_name()
        args = []
        while self.peek_token() != SEMICOLON:
            if self.peek_token() == ",":
                self.skip_token()
                continue
            args.append(self.read_location())
        assert self.read_token() == SEMICOLON
        operation = Operation(op, args)
        if global_scope:
            self.parsed.append(operation)
            self.programme.operations.append(operation)
        return operation

    def read_gate(self):
        assert self.read_token() == GATE
        name = self.read_name()
        args = []
        while self.peek_token() != "{":
            if self.peek_token() == ",":
                self.skip_token()
                continue
            args.append(self.read_token())

        assert self.read_token() == "{"

        operations = []
        while self.peek_token() != "}":
            operations.append(self.read_operation())
        assert self.read_token() == "}"
        self.parsed.append(GateDeclaration(name, args, operations))
        self.programme.gates[name] = GateDefinition(name, args, operations)

    def parse(self):
        self.read_version()
        while self.peek_token():
            token = self.peek_token()
            if token == INCLUDE:
                self.read_include()
            elif token == GATE:
                self.read_gate()
            elif token == QREG:
                self.read_quantum_register()
            elif token == CREG:
                self.read_classical_register()
            elif token == MEASURE:
                self.read_measurement()
            # If none of these match
            else:
                self.read_operation(True)

    def read_quantum_register(self):
        assert self.read_token() == QREG

        name, size = self.read_register_spec_full()
        declaration = QuantumRegisterDeclaration(name, size)

        self.parsed.append(declaration)
        self.programme.quantum_registers[name] = QuantumRegister(size)

    def read_number(self):
        return int(self.read_token())

    def read_register_spec_full(self):
        name = self.read_name()
        assert self.read_token() == "["
        size = self.read_number()
        assert self.read_token() == "]"
        assert self.read_token() == SEMICOLON
        return name, size

    def read_classical_register(self):
        assert self.read_token() == CREG

        name, size = self.read_register_spec_full()
        declaration = ClassicalRegisterDeclaration(name, size)

        self.parsed.append(declaration)
        self.programme.classical_registers[name] = ClassicalRegister(size)

    def read_measurement(self):
        assert self.read_token() == MEASURE
        from_register = self.read_location()
        assert self.read_token() == ARROW
        to_register = self.read_location()
        assert self.read_token() == SEMICOLON
        measurement = Measurement(from_register, to_register)
        self.parsed.append(measurement)
        self.programme.operations.append(measurement)

    def read_location(self):
        name = self.read_name()
        if self.peek_token() == "[":
            assert self.read_token() == "["
            offset = self.read_number()
            assert self.read_token() == "]"
            return RegisterSlice(name, offset)
        else:
            return NamedValue(name)
