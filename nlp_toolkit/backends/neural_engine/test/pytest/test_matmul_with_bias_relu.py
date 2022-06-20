import unittest
from collections import OrderedDict
from nlp_toolkit.backends.neural_engine.compile.ops.op import OPERATORS, Operator
from nlp_toolkit.backends.neural_engine.compile.ops.tensor import Tensor
from nlp_toolkit.backends.neural_engine.compile.graph import Graph
from nlp_toolkit.backends.neural_engine.compile.sub_graph.matmul_with_bias_relu import MatMulWithBiasRelu
import numpy as np


class TestMatmulWithBiasRelu(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass
    
    def test_matmul_with_bias_relu_1(self):
        graph = Graph()
        input_data_node = OPERATORS['Input']()
        input_tensors = []
        output_tensors = [Tensor(), Tensor(), Tensor()]
        input_data_node.construct('input_data', 'Input', input_tensors=input_tensors, 
                                output_tensors=output_tensors)

        mat_node = OPERATORS['MatMulWithBias']()
        input_tensors = [Tensor(data=np.array(1)), Tensor(data=np.array(1)), 
                            Tensor(data=np.array(1))]
        output_tensors = [Tensor(name='matmul:0', source_op=['matmul'], 
                                    dest_op=['relu'])]
        mat_node.construct('matmul', 'MatMulWithBias', input_tensors=input_tensors, 
                                output_tensors=output_tensors, attr=OrderedDict({
                                    'src1_perm': '1,0'}))
        
        tanh_node = OPERATORS['Relu']()
        input_tensors = [Tensor(name='matmul:0', source_op=['matmul'], 
                                    dest_op=['relu'])]
        output_tensors = [Tensor(name='relu:0', source_op=['relu'],
                                dest_op=[])]
        tanh_node.construct('relu', 'Relu', input_tensors=input_tensors, 
                                output_tensors=output_tensors)
        
        graph.insert_nodes(len(graph.nodes), [input_data_node, mat_node, tanh_node])
        graph = MatMulWithBiasRelu()(graph)
        self.assertEqual(2, len(graph.nodes))
        self.assertEqual('1,0', graph.nodes[1].attr['src1_perm'])
        self.assertEqual('relu', graph.nodes[1].name)
        self.assertEqual('relu', graph.nodes[1].attr['append_op'])


if __name__ == "__main__":
    unittest.main()
