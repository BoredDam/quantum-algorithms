from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler
import numpy as np
import sys

def int_to_bin(num: int, code_len: int):
    """
    converts `num` in a binary string, with the specified `code_len`
    """
    num = bin(num)[2:]
    num = '0'*(code_len-len(num)) + num
    return num

def match_operator(n: int):
    '''
    page 12 of the paper
    '''
    qx = QuantumRegister(n, 'x')
    qy = QuantumRegister(n, 'y')
    qout = QuantumRegister(n, 'o')
    qc = QuantumCircuit(qx, qy, qout)
    
    for i in range(n):
        qc.ccx(qx[i], qy[i], qout[i])

    qc.x(qx)
    qc.x(qy)

    for i in range(n):
        qc.ccx(qx[i], qy[i], qout[i])
    
    qc.x(qx)
    qc.x(qy)
    
    return qc.to_gate(label='MATCH')


def extension_operator(n: int, i: int):
    '''
    page 12 of the paper
    '''
    shift = 2 ** (i - 1)

    qin = QuantumRegister(n, 'in')    
    qout = QuantumRegister(n, 'out')
    qc = QuantumCircuit(qin, qout)

    for j in range(n - shift):
        qc.ccx(qin[j], qin[j + shift], qout[j])

    return qc.to_gate(label=f'EXT_{i}')


def quantum_rotation(n: int, s: int):
    '''
    Returns a `.Gate` that implements a rotation
    of `s` positions on `n` qubits lines.
    
    Only works correctly if `s` is a power of 2. Every other
    rotation can be obtained by combination of the power of 2 rotations
    '''
    qr = QuantumRegister(n, 'q')
    qc = QuantumCircuit(qr)
    
    for i in range(1, int(np.ceil(n/2))):
        qc.swap(qr[i], qr[n-i])
    
    for j in range(1, int(np.ceil(n/2))):
        qc.swap(qr[int(np.ceil(s/2))-j], qr[int(np.floor(s/2))+j])

    return qc.to_gate(label='R_'+str(s)+' ')


def quantum_parametric_rotation(n: int):
    '''
    Returns an arbitrary rotation `.Gate` on `n` qubits lines.

    page 9 of the paper
    '''
    l = int(np.ceil(np.log2(n)))

    jr = QuantumRegister(l, 'j')
    qr = QuantumRegister(n, 'q')

    qc = QuantumCircuit(jr, qr)
    for i in range(l):
        
        qc = qc.compose(quantum_rotation(n, 2**i).control(1), [i,*qr])
    return qc


def copy_operator(n: int):
    '''
    page 13 of the paper
    '''
    qin = QuantumRegister(n, 'in')
    qout = QuantumRegister(n, 'out')
    qc = QuantumCircuit(qin, qout)

    for i in range(n):
        qc.cx(qin[i], qout[i])
    
    
    return qc.to_gate(label='COPY')


def or_operator(n: int):
    '''
    page 15 of the paper
    '''
    qx = QuantumRegister(n, 'x')
    qy = QuantumRegister(1, 'y')
    qc = QuantumCircuit(qx, qy)
    
    qc.x(qx)
    qc.mcx(qx, qy)
    qc.x(qx)
    qc.x(qy)

    return qc.to_gate(label='OR')


def contr_bitwise_and_operator(n: int):
    '''
    page 13 of the paper
    '''
    qc_ctrl = QuantumRegister(1, 'c')
    qL = QuantumRegister(n, 'L')
    qin = QuantumRegister(n+1, 'qin')
    qout  = QuantumRegister(n+1, 'qout')
    qc = QuantumCircuit(qc_ctrl, qL, qin, qout)

    for k in range(n):
        qc.mcx([qc_ctrl[0], qL[k], qin[k]], qout[k])

    return qc.to_gate(label="C-AND")


def FSM(n):
    '''
    builds the Fixed Substring Matching operator for inputs of size `n`
    '''
    
    d_len = int(np.ceil(np.log2(n)))
    L_num = d_len
    qx = QuantumRegister(n, 'x')
    qy = QuantumRegister(n, 'y')
    qd = QuantumRegister(d_len, 'd')
    qD = QuantumRegister(d_len+1, 'D')
    qL = []

    for i in range(L_num): # padding
        qL.append(QuantumRegister(n, 'L['+str(i)+']'))
    
    qD = []
    for i in range(d_len+1):
        qD.append(QuantumRegister(n+1, 'D['+str(i-1)+']'))
    
    qr = QuantumRegister(1, 'r')
    qc = QuantumCircuit(qx,qy,qd,*qL,*qD,qr)
    

    qc = qc.compose(match_operator(n), [*qx, *qy, *qL[0]])
    
    for i in range(L_num-1):
        qc = qc.compose(extension_operator(n, i+1), [*qL[i][:n], *qL[i+1]])
    
    for i in range(d_len):
        
        qc = qc.compose(contr_bitwise_and_operator(n), [qd[i], *qL[i], *qD[i], *qD[i+1]])
        
        controlled_rot = quantum_rotation(n+1, 2**i).control(1)
        qc = qc.compose(controlled_rot, [qd[i], *qD[i+1]])
        qc.x(qd[i])
        controlled_copy = copy_operator(n+1).control(1)
        qc = qc.compose(controlled_copy, [qd[i],*qD[i], *qD[i+1]])
        qc.x(qd[i])

    qc = qc.compose(or_operator(n+1), [*qD[d_len], qr])

    return qc


def SFC(n):
    '''
    builds the Shared Fix Substring Check operator for inputs of size `n`
    '''
    d_len = int(np.ceil(np.log2(n)))
    L_num = d_len
    qx = QuantumRegister(n, 'x')
    qy = QuantumRegister(n, 'y')
    qd = QuantumRegister(d_len, 'd')
    qD = QuantumRegister(d_len+1, 'D')
    qL = []

    for i in range(L_num): # padding
        qL.append(QuantumRegister(n, 'L['+str(i)+']'))
    
    qD = []
    for i in range(d_len+1):
        qD.append(QuantumRegister(n+1, 'D['+str(i-1)+']'))
    
    qr = QuantumRegister(1, 'r')
    qc = QuantumCircuit(qx,qy,qd,*qL,*qD,qr)
    
    qc.x(qD[0])

    qc = qc.compose(FSM(n))
    return qc


def FPM(n):
    '''
    builds the Fixed Prefix Matching operator for inputs of size `n`
    '''

    d_len = int(np.ceil(np.log2(n)))
    L_num = d_len
    qx = QuantumRegister(n, 'x')
    qy = QuantumRegister(n, 'y')
    qd = QuantumRegister(d_len, 'd')
    qD = QuantumRegister(d_len+1, 'D')
    qL = []

    for i in range(L_num): # padding
        qL.append(QuantumRegister(n, 'L['+str(i)+']'))
    
    qD = []
    for i in range(d_len+1):
        qD.append(QuantumRegister(n+1, 'D['+str(i-1)+']'))
    
    qr = QuantumRegister(1, 'r')
    qc = QuantumCircuit(qx,qy,qd,*qL,*qD,qr)
    
    # init
    qc.x(qD[0][0])
    
    qc = qc.compose(FSM(n))
    return qc


def grover_operator(n: int):
    '''
    builds the diffusion operator from the grover algorithm
    '''
    qx = QuantumRegister(n, 'x')
    qc = QuantumCircuit(qx)
    
    qc.h(qx)
    qc.x(qx)
    qc.h(qx[n-1])
    qc.mcx(qx[list(range(n-1))], qx[n-1])
    qc.h(qx[n-1])
    qc.x(qx)
    qc.h(qx)

    return qc.to_gate(label='DIFFUSION')


def quantum_number_encode(num: int, code_len: int=0):
    """
    encodes the given `num` into a quantum circuit. if specified, `code_len` lets
    you use more qubits than needed for the number specified by `num`
    """
    if num == 0:
        return QuantumCircuit(code_len).to_gate(label=" 0 ")
        
    if code_len < int(np.ceil(np.log2(num))):
        code_len = bin_num
    bin_num = int_to_bin(num, code_len)
    qc = QuantumCircuit(code_len)
    for c, i in enumerate(bin_num):
        if i == '1':
            qc.x(code_len-1-c)
    return qc.to_gate(label=" "+str(num)+" ")


def encode_boolean_string(x: str):
    n = len(x)
    qx = QuantumRegister(n, 'x')
    qc = QuantumCircuit(qx)

    for c, i in enumerate(x):
        if i == '1':
            qc.x(qx[n - c - 1])
    
    return qc


def quantum_step_circuit(n: int, d: int, x: str, y: str):

    qi_amount = int(np.ceil(np.log2(n)))
    qi = QuantumRegister(qi_amount, 'i')
    qj = QuantumRegister(qi_amount, 'j')
    qx = QuantumRegister(n, 'x')
    qy = QuantumRegister(n, 'y')
    ancilla_amount = n * int(np.ceil(np.log2(n))) + (n+1)*(int(np.ceil(np.log2(n+1))))
    qa = QuantumRegister(ancilla_amount, 'a')
    qd = QuantumRegister(qi_amount, 'd')
    qr = QuantumRegister(1, 'r')
    qo = QuantumRegister(1, 'out')

    c = ClassicalRegister(1,'c')
    qc = QuantumCircuit(qi,qj,qx,qy,qa,qd,qr,qo, c)

    qc = qc.compose(quantum_number_encode(d,qi_amount), qd)
    qc = qc.compose(encode_boolean_string(x), qx)
    qc = qc.compose(encode_boolean_string(y), qy)
    qc.barrier(label='init')
    
    # search phase
    qc.h(qj)
    qc.x(qo)
    qc.h(qo)
    
    epochs = int(np.floor(np.pi/4 * np.sqrt(n)))
    
    for e in range(epochs):
        qc = qc.compose(quantum_parametric_rotation(n).to_gate(label='ROT'), [*qj,*qx])
        qc = qc.compose(SFC(n).to_gate(label='SFC'), [*qx, *qy, *qd, *qa, qr])

        qc.cx(qr, qo)
        qc = qc.compose(SFC(n).inverse().to_gate(label='- SFC'), [*qx, *qy, *qd, *qa, qr])
        qc = qc.compose(quantum_parametric_rotation(n).inverse().to_gate(label='- ROT'), [*qj,*qx])

        qc = qc.compose(grover_operator(qi_amount), qj)

    qc.measure(qj[1], c)
    qc.measure(qj[0], c)
    qc.h(qo)
    qc.x(qo)
    qc.barrier(label='SEARCH PHASE')

    qc.h(qi)

    # verification phase
    qc.x(qo)
    qc.h(qo)
    for e in range(epochs):
        qc = qc.compose(quantum_parametric_rotation(n).to_gate(label='ROT'), [*qj,*qx])
        qc = qc.compose(quantum_parametric_rotation(n).to_gate(label='ROT'), [*qi,*qx])
        qc = qc.compose(quantum_parametric_rotation(n).to_gate(label='ROT'), [*qi,*qy])
        qc = qc.compose(FPM(n).to_gate(label='FPM'), [*qx, *qy, *qd, *qa, qr])

        qc.cx(qr, qo)
        qc = qc.compose(FPM(n).inverse().to_gate(label='- FPM'), [*qx, *qy, *qd, *qa, qr])
        qc = qc.compose(quantum_parametric_rotation(n).inverse().to_gate(label='- ROT'), [*qi,*qy])
        qc = qc.compose(quantum_parametric_rotation(n).inverse().to_gate(label='- ROT'), [*qi,*qx])
        qc = qc.compose(quantum_parametric_rotation(n).inverse().to_gate(label='- ROT'), [*qj,*qx])

        qc = qc.compose(grover_operator(qi_amount), qi)

    qc.measure(qj[1], c)
    qc.measure(qj[0], c)
    qc.barrier(label='VERIFICATION PHASE')

    # final check
    qc.h(qo)
    qc.x(qo)
    
    for e in range(epochs):
        qc = qc.compose(quantum_parametric_rotation(n).to_gate(label='ROT'), [*qj,*qx])
        qc = qc.compose(quantum_parametric_rotation(n).to_gate(label='ROT'), [*qi,*qx])
        qc = qc.compose(quantum_parametric_rotation(n).to_gate(label='ROT'), [*qi,*qy])
        qc = qc.compose(FPM(n).to_gate(label='FPM'), [*qx, *qy, *qd, *qa, qr])

        qc.cx(qr, qo)
        qc = qc.compose(FPM(n).inverse().to_gate(label='- FPM'), [*qx, *qy, *qd, *qa, qr])
        qc = qc.compose(quantum_parametric_rotation(n).inverse().to_gate(label='- ROT'), [*qi,*qy])
        qc = qc.compose(quantum_parametric_rotation(n).inverse().to_gate(label='- ROT'), [*qi,*qx])
        qc = qc.compose(quantum_parametric_rotation(n).inverse().to_gate(label='- ROT'), [*qj,*qx])

    qc.measure(qo, c)
    qc.barrier(label='FINAL CHECK')

    return qc  


def run(qc, shots=1024):
    """
    ritorna i risultati dell'esecuzione del `qc` `QuantumCircuit` nel simulatore ideale AerSimulator. 
    `shots` permette di specificare il numero di esecuzioni da compiere.
    """
    sim_backend = AerSimulator(method='matrix_product_state')
    
    pm = generate_preset_pass_manager(backend=sim_backend, optimization_level=2)
    isa_qc = pm.run(qc)
    sampler = Sampler(mode=sim_backend)

    job = sampler.run([isa_qc], shots=shots)
    results = job.result()
    data = results[0].data
    counts = data.c.get_counts()

    return counts


def quantum_LCS_test(n: int, d: int, x: str, y: str):
    
    if d == 0: # esiste sempre una sottostringa comune di dimensione 0
        return True 

    qc = quantum_step_circuit(n, d, x, y)
    qc.draw('mpl')
    c = run(qc, 20)
    
    if '1' in list(c.keys()):
        return True
    else:
        return False


def quantum_LCS(x: str, y: str, n: int, verbose=False):
    l = 0
    r = n
    last = n
    while l < r:
        d = int(np.floor((l + r) / 2 ))
        if d == last:
            return l
        
        if verbose:
            print(f"testing for common substring of length {d}:", end=" ")

        if quantum_LCS_test(n, d, x, y):
            l = d
            if verbose: print("found!")
        else:
            r = d
            if verbose: print("not found!")
        last = d
    return l



if len(sys.argv) != 3:
    print("correct usage: QLCS.py <string1> <string2>\nquitting...")
    exit(0)

X, Y = str(sys.argv[1]), str(sys.argv[2])


print(f"Looking for the LCS of strings X:'{X}', Y:'{Y}'")

quantum_LCS(X, Y, 4, verbose=True)

print(
"""
a project by Damiano Trovato, based on the work of Cantone Domenico, 
Faro Simone, Pavone Arianna & Viola Caterina. (2023).""")

