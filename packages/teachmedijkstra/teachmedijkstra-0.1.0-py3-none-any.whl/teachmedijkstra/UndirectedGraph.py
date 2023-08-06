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
Definition of class `UndirectedGraph` which represents an undirected weighted
    graph.
"""

__all__ = ["UndirectedGraph"]

import teachmedijkstra.DirectedGraph

class UndirectedGraph(teachmedijkstra.DirectedGraph):
    r"""
    Represents an undirected weighted graph.

    This class implements some basic methods to work with an undirected graph
    and, most of all, methods to draw the graph either using the TikZ library
    or the PSTricks library of LaTeX.

    Definition:
        An *undirected weighted graph* consists of:

          * V ... a set of vertices,
          * E ... a set of edges,
          * p: E -> {{a,b} | a,b in V} ... an *incidence function* that maps
              each edge to an unordered pair of vertices,
          * w: E -> R ... a *weight function* that maps each edge to a positive
              real number.

    An undirected graph, represented by this class, is basically a directed
    graph represented by `teachmedijkstra.DirectedGraph` where each edge (a, b) with weight w
    has its counterpart (b, a) with the same weight w.
    See the method `UndirectedGraph.addEdge`.
    """

    def getNumberOfEdges(self):
        """
        Returns:
            int: the number of the edges of the graph
        """
        return super().getNumberOfEdges() // 2

    def addEdge(self, initial, terminal, value, tikzOptions = ""):
        """
        Adds a new undirected edge to the graph.

        This, actually, consists in adding two directed edges:
        (initial, terminal) and (terminal, initial).

        As in `DirectedGraph.addEdge`, if an edge with the given vertices is
        already present in the graph, nothing is created.

        Args:
            initial (str): the name of the first vertex of the edge
            terminal (str): the name of the second vertex of the edge
            weight (float): weight of the edge
            tikzOptions (str): additional options determining how the edge will
                be drawn by TikZ
        """
        #teachmedijkstra.DirectedGraph.addEdge(self, initial, terminal, value, tikzOptions)
        #teachmedijkstra.DirectedGraph.addEdge(self, terminal, initial, value, tikzOptions)
        super().addEdge(initial, terminal, value, tikzOptions)
        super().addEdge(terminal, initial, value, tikzOptions)

    # ========================================================================================
    # TikZ
    # ========================================================================================

    def exportEdgeToTikZ(
            self,
            initial,
            terminal,
            showWeight = True,
            edgeStyle = "graph edge directed",
            additionalTikZOptions = "",
            indent = "",
            indentTab = "    "):
        """
        Args:
            initial (str): the initial vertex of the edge
            terminal (str): the terminal vertex of the edge
            showWeight (bool, optional): if `True` then the weight will be
                written to the image
            edgeStyle (str): the initial TikZ option of this edge;
                one of the TikZ styles defined in
                `DirectedGraph.exportHeadToTikZ`
            additionalTikZOptions (str): additional options determining how the
                edge will be drawn by TikZ
            indent (str, optional): text written at the beginning of each line
                to perform indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform
                indenting of more nested parts of the resulting LaTeX code
                (by default: string with four spaces)

        Returns:
            str: TikZ code to draw an edge of this graph
        """
        return super().exportEdgeToTikZ(
            initial,
            terminal,
            showWeight = showWeight,
            edgeStyle = "graph edge undirected",
            additionalTikZOptions = additionalTikZOptions,
            indent = indent,
            indentTab = indentTab)

    def exportEdgesToTikZ(
            self,
            showWeight = True,
            edgeStyle = "graph edge undirected",
            additionalTikZOptions = "",
            indent = "",
            indentTab = "    "):
        """
        This method rewrites the code of `DirectedGraph.exportEdgesToTikZ` in
        order not to draw an undirected edge twice.

        Args:
            showWeight (bool, optional): if `True` then the weight will be
                written to the image
            edgeStyle (str): the initial TikZ option of the edges;
                one of the TikZ styles defined in
                `DirectedGraph.exportHeadToTikZ`
            additionalTikZOptions (str): additional options determining how the
                edges will be drawn by TikZ
            indent (str, optional): text written at the beginning of each line
                to perform indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform
                indenting of more nested parts of the resulting LaTeX code
                (by default: string with four spaces)

        Returns:
            str: TikZ code to draw the edges of this graph
        """
        text = ""
        for vertex in self.edges:
            for neighbour in self.edges[vertex]:
                if vertex < neighbour:
                    text += self.exportEdgeToTikZ(
                            vertex,
                            neighbour,
                            showWeight = showWeight,
                            edgeStyle = edgeStyle,
                            indent = indent,
                            indentTab = indentTab)
        return text

    def exportToTikZ(
            self,
            showWeight = True,
            edgeStyle = "graph edge undirected",
            includeTikZDefinitions = True,
            additionalTikZOptionsForVertices = "",
            additionalTikZOptionsForEdges = "",
            indent = "",
            indentTab = "    "):
        """
        This method rewrites the code of `DirectedGraph.exportToTikZ` in
        order not to draw undirected edges twice.

        Args:
            showWeight (bool, optional): if `True` then the weight of the edges
                will be written to the image
            edgeStyle (str): the initial TikZ option of the edges of the graph;
                one of the TikZ styles defined in
                `DirectedGraph.exportHeadToTikZ`
            includeTikZDefinitions (bool, optional): if `True` then the TikZ
                definitions of graph nodes and edges will be included to the head
                of the TikZ image
            additionalTikZOptionsForVertices (str): additional options
                determining how the vertices will be drawn by TikZ
            additionalTikZOptionsForEdges (str): additional options determining
                how the edges will be drawn by TikZ
            indent (str, optional): text written at the beginning of each line
                to perform indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform
                indenting of more nested parts of the resulting LaTeX code
                (by default: string with four spaces)

        Returns:
            str: TikZ code to draw this graph
        """
        return super().exportToTikZ(
            showWeight = showWeight,
            edgeStyle = "graph edge undirected",
            includeTikZDefinitions = includeTikZDefinitions,
            additionalTikZOptionsForVertices = additionalTikZOptionsForVertices,
            additionalTikZOptionsForEdges = additionalTikZOptionsForEdges,
            indent = indent,
            indentTab = indentTab)


