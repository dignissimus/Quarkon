from Quarkon.debug import debug_object


class Entanglement:  # TODO: I want typed params but circular imports
    def __init__(self, parent, child, gate):
        self.parent = parent
        self.child = child
        self.gate = gate

    def debug(self):
        debug_object(self)
