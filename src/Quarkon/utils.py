from Quarkon.qubit import Qubit


def abstract(func):
    def wrapper(*args, **kwargs):
        raise NotImplementedError(f"Function '{func.__name__}' has not been implemented")

    return wrapper


def circuit(original_name=None):
    def _param_wrapper(func):
        def wrapper(*qubits, repeat=1000, name=original_name, analyse=True):
            if name is None:
                name = func.__name__

            newbits = []
            for qubit in qubits:
                if type(qubit) is Qubit:
                    newbits.append(qubit)
                elif type(qubit) is int and qubit in [0, 1]:  # Qubit is 1 or 0
                    newbits.append(
                        Qubit.from_probability(1 - qubit, qubit))  # TODO: Works for positive integers at least
                else:
                    raise TypeError("Expected a Qubit or an integer equal to One or zero")

            results = []
            for i in range(repeat):
                testcases = []
                for newbit in newbits:
                    testcases.append(newbit.copy())
                testcases = tuple(testcases)

                try:
                    result = func(*testcases)
                except TypeError:
                    result = func(testcases)
                results.append(result)

            if analyse:
                print(f"{name}\n----------")
                uniques = set(results)
                for unique in uniques:
                    print(f"{unique} = {results.count(unique)/len(results)*100}%")

        return wrapper

    return _param_wrapper
