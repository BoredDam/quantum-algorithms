# QRAM

A naive implementation of a Quantum data structure: the Quantum-RAM (also known as Quantum Vector). 
The idea is to have an operator that, given an array $V = [v_0, v_1, \dots, v_{-1}]$, behaves like:

$$
QRAM \ket{i}\ket{0} \to \ket{i}\ket{v[i]}
$$

The QRAM operator is implemented as an oracle. Access to the QRAM can be made in superposition
by using the Hadamard gate on the index lines.

$$
QRAM \ket{+}\ket{0} \to  \frac{1}{\sqrt{2^n}}\sum_{i \in \\{0,1\\}^n}(\ket{i}\ket{v[i]})
$$

You can also use Grover search algorithm to search in 
$\tilde{\mathcal{O}}(\sqrt N)$ time the position of a given number ($N = 2^n$, with $n$ qubits).
