# -*- coding: UTF-8 -*-

# This file is a part of teachmedijkstra which is a Python3 package designed
# for educational purposes to demonstrate the Quine-McCluskey algorithm.
#
# Copyright (C) 2021 Milan Petrík <milan.petrik@protonmail.com>
#
# Web page of the program: <https://gitlab.com/petrikm/teachmedijkstra>
#
# teachmedijkstra is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# teachmedijkstra is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# teachmedijkstra. If not, see <https://www.gnu.org/licenses/>.

"""
This package contains an implementation of the Dijkstra's algorithm for finding
the shortest paths in a graph and serves to educational purposes.

Its main goal is to produce a LaTeX document which contains:

  * description of the performing of the Dijkstra's algorithm in a for of a
    table where each row corresponds to a vertex of the graph and each column
    corresponds to one time step of the algorithm,
  * shortest path tree (or shortest path covering) which is a subgraph of the
    processed graph that contains those edges that belong the shortest paths.

The main motivation to write this program was to have a tool to automatically
generate examen tests on Dijkstra's algorithm with randomly created graphs and
with the corresponding solutions which consist of two items described in the
list above.

A simple program using this package may look like this:

    import teachmedijkstra

    graph = teachmedijkstra.UndirectedGraph()
    graph.addVertex("a", (0,2))
    graph.addVertex("b", (1,2))
    graph.addVertex("c", (2,2))
    graph.addVertex("d", (0,1))
    graph.addVertex("e", (1,1))
    graph.addVertex("f", (2,1))
    graph.addEdge("a", "b", 7)
    graph.addEdge("b", "c", 8)
    graph.addEdge("d", "e", 6)
    graph.addEdge("e", "f", 1)
    graph.addEdge("a", "d", 5)
    graph.addEdge("b", "e", 2)
    graph.addEdge("c", "f", 4)
    graph.addEdge("a", "e", 3)
    graph.addEdge("b", "f", 9)

    dijkstra = teachmedijkstra.Dijkstra(graph, "a")
    dijkstra.run()

    dijkstra.saveToLaTeXFile("example.tex")

The presented code defines an undirected weighted graph with six vertices,
performs the Dijkstra's algorithm to find the shortest paths starting from the
vertex "a", and exports the result to a LaTeX file "example.tex".
"""

from teachmedijkstra.DirectedGraph import *
from teachmedijkstra.UndirectedGraph import *
from teachmedijkstra.Dijkstra import *
from teachmedijkstra.Utils import *
from teachmedijkstra.Constants import *
