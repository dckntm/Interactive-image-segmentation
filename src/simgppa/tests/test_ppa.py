import io
import os
import unittest
from pathlib import Path
from typing import List

from simgppa.ppa import PPA, Edge

path = os.path.abspath(__file__)


def load(num: int):
    p = Path(path).parent.joinpath(f'data/test_{num}.txt')

    with open(p) as input:
        vertex_num, edge_num = input.readline().split()
        vertex_num, edge_num = int(vertex_num),  int(edge_num)

        edges: List[Edge] = []

        for _ in range(edge_num):
            s, e, c = input.readline().split()
            s, e, c = int(s)-1, int(e)-1, int(c)

            edges.append(Edge(s, e, c))

    return vertex_num, edges


class Test_PPA(unittest.TestCase):
    def test_1(self):

        vertex_num, edges = load(1)

        result = PPA(vertex_num, edges).maxflow()

        self.assertEqual(result, 935)

    def test_2(self):

        vertex_num, edges = load(2)

        result = PPA(vertex_num, edges).maxflow()

        self.assertEqual(result, 2789)

    def test_3(self):

        vertex_num, edges = load(3)

        result = PPA(vertex_num, edges).maxflow()

        self.assertEqual(result, 2000000)

    def test_4(self):

        vertex_num, edges = load(4)

        self.assertRaises(
            Exception,
            lambda: PPA(vertex_num, edges).maxflow())

    def test_5(self):

        vertex_num, edges = load(5)

        self.assertRaises(
            AttributeError,
            lambda: PPA(vertex_num, edges).maxflow())

    def test_6(self):

        vertex_num, edges = load(6)

        self.assertRaises(
            Exception,
            lambda: PPA(vertex_num, edges).maxflow())
