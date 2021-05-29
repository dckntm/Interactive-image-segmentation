import io
import os
import unittest
from pathlib import Path
from typing import List

from simgppa.ppa import PPA, Edge

path = os.path.abspath(__file__)


def load(pref: str):
    p = Path(path).parent.joinpath(f'data/ppa/test_{pref}.txt')

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

        result = PPA(vertex_num, edges).max_flow()

        self.assertEqual(result, 935)

    def test_2(self):

        vertex_num, edges = load(2)

        result = PPA(vertex_num, edges).max_flow()

        self.assertEqual(result, 2789)

    def test_3(self):

        vertex_num, edges = load(3)

        result = PPA(vertex_num, edges).max_flow()

        self.assertEqual(result, 2000000)

    def test_4(self):

        vertex_num, edges = load(4)

        result = PPA(vertex_num, edges).max_flow()

        self.assertEqual(result, 23)

    def test_5(self):

        vertex_num, edges = load(5)

        result = PPA(vertex_num, edges).max_flow()

        self.assertEqual(result, 256)

    def test_6(self):

        vertex_num, edges = load(6)

        result = PPA(vertex_num, edges).max_flow()

        self.assertEqual(result, 523)


class Test_PPA_D(unittest.TestCase):
    def test_1(self):

        vertex_num, edges = load('d1')

        result = PPA(vertex_num, edges).max_flow()

        self.assertEqual(result, 935)

    def test_2(self):

        vertex_num, edges = load('d2')

        result = PPA(vertex_num, edges).max_flow()

        self.assertEqual(result, 2789)

    def test_3(self):

        vertex_num, edges = load('d3')

        result = PPA(vertex_num, edges).max_flow()

        self.assertEqual(result, 2000000)

    def test_4(self):

        vertex_num, edges = load('d4')

        result = PPA(vertex_num, edges).max_flow()

        self.assertEqual(result, 2000000)

    def test_5(self):

        vertex_num, edges = load('d5')

        result = PPA(vertex_num, edges).max_flow()

        self.assertEqual(result, 3278)
