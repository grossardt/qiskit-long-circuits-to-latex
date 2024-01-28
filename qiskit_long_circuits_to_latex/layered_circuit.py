# Copyright Andre Grossardt 2022-2024
# Licensed under the MIT license, see LICENSE.txt for details

"""LayeredCircuit class for printing circuits over multiple lines in LaTeX."""

from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit

class LayeredCircuit:
    """Turn ciruit into list of circuits of depth 1 for printing over multiple lines.
    
    Main usage for printing circuits in LaTeX with n gates per line:
    ``LayeredCircuit(circuit).multiline_latex(n)``

    The argument ``circuit`` can be a QuantumCircuit, LayeredCircuit, or a list of such.
    """
    
    def __init__(self, circuits = []):
        self._current_index = 0
        self._layers = []
        self.num_qubits = 0
        arg_error  = 'Argument must be one of QuantumCircuit, LayeredCircuit, '
        arg_error += 'or list of QuantumCircuits of equal size.'
        if isinstance(circuits, QuantumCircuit):
            circuits = [circuits]
        if isinstance(circuits, LayeredCircuit):
            circuits = circuits._layers
        if not isinstance(circuits, list):
            raise TypeError(arg_error)
        if circuits:
            self.num_qubits = len(circuits[0].qubits)
        for circuit in circuits:
            if not isinstance(circuit, QuantumCircuit):
                raise TypeError(arg_error)
            if not len(circuit.qubits) == self.num_qubits:
                raise TypeError(arg_error)
            dag = circuit_to_dag(circuit)
            for layer in dag.layers():
                qc = dag_to_circuit(layer['graph'])
                qc.global_phase = 0 # ignore all global phases
                self._layers.append(qc)
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index < len(self.layers):
            l = self._layers[self._current_index]
            self._current_index += 1
            return l
        else:
            raise StopIteration
            
    def __getitem__(self, i):
        if isinstance(i, slice):
            return LayeredCircuit(self._layers[i])
        elif isinstance(i, int): # if an index is passed, return single circuit
            return self._layers[i]
        else:
            raise TypeError('Invalid argument type.')
    
    def __len__(self):
        return len(self._layers)
    
    def append(self, other):
        """Appends another LayeredCircuit"""
        if not isinstance(other, LayeredCircuit):
            other = LayeredCircuit(other)
        for layer in other:
            self._layers.append(layer)
    
    def merge(self):
        """Returns the merged QuantumCircuit of all layers"""
        qc = QuantumCircuit(self.num_qubits)
        for layer in self._layers:
            qc.compose(layer,range(self.num_qubits),inplace=True)
        return qc
        
    def draw(self, *args, **kwargs):
        """Draws the merged circuit, same syntax as QuantumCircuit.draw()"""
        return self.merge().draw(*args, **kwargs)
    
    def latex(self):
        """Returns LaTeX Qcircuit code."""
        doc = self.draw('latex_source')
        return '\\Qcircuit' + doc.split('\\Qcircuit')[1].split('}\n\\end{document}')[0]
    
    def multiline_latex(self, gates_per_line = 10, latex_font_size = 'tiny'):
        """Returns Qcircuit LaTeX code to print a circuit over multiple lines
        with specified number of gates per line."""
        output = ''
        for i in range(len(self) // gates_per_line + 1):
            start = i*gates_per_line
            stop = min(len(self),(i+1)*gates_per_line)
            output += '&\\begin{array}{c}\\' + latex_font_size + '\n'
            output += self[start:stop].latex()
            output += '\n\\end{array}\\nonumber\\\\\n'
        return output