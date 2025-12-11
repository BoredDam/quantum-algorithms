from qiskit import QuantumCircuit, QuantumRegister
import numpy as np

def int_to_bin(num: int, code_len: int):
    """
    converts `num` in a binary string, with the specified `code_len`
    """
    num = bin(num)[2:]
    num = '0'*(code_len-len(num)) + num
    return num


def quantum_number_encode(num: int, code_len: int=0):
    """
    encodes the given `num` into a quantum circuit. if specified, `code_len` lets
    you use more qubits than needed for the number specified by `num`
    """
    if code_len < int(np.ceil(np.log2(num))):
        code_len = bin_num
    bin_num = int_to_bin(num, code_len)
    qc = QuantumCircuit(code_len)
    for c, i in enumerate(bin_num):
        if i == '1':
            qc.x(code_len-1-c)
    return qc.to_gate(label=" "+str(num)+" ")