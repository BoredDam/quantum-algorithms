from qiskit import QuantumCircuit, QuantumRegister

def general_boolean_oracle(n: int, sol: list[str]):
    """
    generates a general boolean oracle of size qubits given the list
    of inputs for which it should output 1
    """
    xr = QuantumRegister(n,'x')
    yr = QuantumRegister(1,'out')
    qc = QuantumCircuit(xr, yr)    
    
    for s in sol:
        for i in range(n):
            if s[i]=='0':
                qc.x(xr[i])
        qc.mcx(xr,yr[0])
        for i in range(n):
            if s[i]=='0':
                qc.x(xr[i])
    qc = qc.to_gate(label='  oracle  ')
    return qc    

def bernstein_vazirani_oracle(s: str, is_little_endian: bool = True):
    """
    generates the oracle of the bernstein varizani circuit
    given a `s` string. If not specified by `is_little_endian`, 
    it follows the little endianess of Qiskit.
    """
    n = len(s)
    xr = QuantumRegister(n,'x')
    yr = QuantumRegister(1,'out')
    qc = QuantumCircuit(xr, yr)    
    if is_little_endian:
        for c, i in enumerate(s, 0):
            if i == '1':
                qc.cx(n-c-1, yr) # n-c-1 to adapt to the big endian of qiskit
    else:
        for c, i in enumerate(s, 0):
            if i == '1':
                qc.cx(c, yr) 
    qc = qc.to_gate(label='  oracle  ')
    
    return qc