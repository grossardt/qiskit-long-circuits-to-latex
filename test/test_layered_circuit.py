# Copyright Andre Grossardt 2024
# Licensed under the MIT license, see LICENSE.txt for details

"""
Tests for the layered circuit class
"""
import unittest
from qiskit import QuantumCircuit
from qiskit_long_circuits_to_latex import LayeredCircuit

class TestLayeredCircuit(unittest.TestCase):
    """Tests for the layered circuit class"""
    def test_printing(self):
        qc = QuantumCircuit(2)
        for _ in range(7):
            qc.h(0)
            qc.cx(0, 1)
            qc.y(1)
        latex = LayeredCircuit(qc).multiline_latex(gates_per_line = 10, latex_font_size='test')
        split = latex.split('\n')
        self.assertEqual(len(split), 13)
        self.assertEqual(split[0], '&\\begin{array}{c}\\test')
        self.assertEqual(split[1], '\\Qcircuit @C=1.0em @R=0.2em @!R { \\\\')
        self.assertEqual(split[-3], '\\\\ }')
        self.assertEqual(split[-2], '\\end{array}\\nonumber\\\\')
        self.assertEqual(split[-1], '')

if __name__ == "__main__":
    unittest.main()
