# qiskit-long-circuits-to-latex
 Implements a simple Python class to export long Qiskit quantum circuits into a multi-line
 LaTeX QCircuit environment.

## Usage

```python
from qiskit import QuantumCircuit
from qiskit_long_circuits_to_latex import LayeredCircuit

circuit = # some deep Qiskit circuit
latex = LayeredCircuit(circuit).multiline_latex(gates_per_line = 15)
```
