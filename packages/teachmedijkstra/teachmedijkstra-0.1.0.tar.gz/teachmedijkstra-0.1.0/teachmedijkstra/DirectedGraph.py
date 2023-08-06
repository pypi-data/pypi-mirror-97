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
Definition of class `DirectedGraph` which represents a directed weighted graph.
"""

__all__ = ["DirectedGraph"]

class DirectedGraph:
    r"""
    Represents a directed weighted graph.

    This class implements some basic methods to work with a directed graph and,
    most of all, methods to draw the graph either using the TikZ library or the
    PSTricks library of LaTeX.

    Definition:
        A *directed weighted graph* consists of:

          * V ... a set of vertices,
          * E ... a set of edges,
          * p: E -> V x V ... an *incidence function* that maps each edge to an
              ordered pair of vertices,
          * w: E -> R ... a *weight function* that maps each edge to a positive
              real number.

    Example:
        The following code creates a directed graph with 6 vertices and 8 edges
        and exports it to a LaTeX document as a TikZ image.
        Notice that additional TikZ options can be attached to the definition
        of an edge.

            import teachmedijkstra.DirectedGraph

            graph = teachmedijkstra.DirectedGraph()
            graph.addVertex("a", (0, 1))
            graph.addVertex("b", (1, 1))
            graph.addVertex("c", (2, 1))
            graph.addVertex("d", (0, 0))
            graph.addVertex("e", (1, 0))
            graph.addVertex("f", (2, 0))
            graph.addEdge("a", "b", 5)
            graph.addEdge("b", "c", 3)
            graph.addEdge("d", "e", 4)
            graph.addEdge("e", "f", 2)
            graph.addEdge("a", "d", 1)
            graph.addEdge("b", "e", 9)
            graph.addEdge("c", "f", 7)
            graph.addEdge("d", "f", 8, "bend right=60, swap")

            graph.saveToLaTeXFile("example.tex")

    Attributes:
        vertices (dict of 2-tuples of int): the key of each item is a string
            which represents the name of the vertex;
            the tuple `(x, y)` is the position of the vertex (needed when the
            graph is drawn utilizing TikZ or PSTricks)
        edges (dict of dict of float): dict with two keys;
            the first key is a string that represents the name of the first
            vertex of the directed edge;
            analogously, the second key represents the second vertex;
            the value is the weight of the edge;
            if an edge does not exist then the corresponding pair of keys is
            not present in the dict
        edgesOptions (dict of dict of str): dict with the same key structure as
            `edges`, however, the values contain strings with additional TikZ
            options for each edge
    """

    def __init__(self):
        """
        The constructor creates an empty graph, i.e., the set of vertices and
        the set of edges are both empty.
        """
        self.vertices = {}
        self.edges = {}
        self.edgesOptions = {}

    def getNumberOfVertices(self):
        """
        Returns:
            int: the number of the vertices of the graph
        """
        return len(self.vertices)

    def getNumberOfEdges(self):
        """
        Returns:
            int: the number of the edges of the graph
        """
        result = 0
        for firstVertex in self.edges:
            result += len(self.edges[firstVertex])
        return result

    def addVertex(self, name, coordinates = (0, 0)):
        """
        Adds a new vertex to the graph.

        Args:
            name (str): vertex name;
                must differ from the other names of the vertices of this graph
            coordinates (2-tuple of int): position of the vertex;
                needed when exporting the graph utilizing TikZ or PSTricks
        """
        self.vertices[name] = coordinates

    def addEdge(self, initial, terminal, weight, tikzOptions = ""):
        """
        Adds a new directed edge to the graph.

        However, if an edge with this initial and terminal vertex is already
        present in the graph, nothing is created.

        Args:
            initial (str): the name of the initial vertex of the edge
            terminal (str): the name of the terminal vertex of the edge
            weight (float): weight of the edge
            tikzOptions (str): additional options determining how the edge will
                be drawn by TikZ
        """
        #TODO throw an exception if an edge with this initial and terminal
        # vertex already exists in the graph
        if not initial in self.edges:
            self.edges[initial] = {}
        if not terminal in self.edges[initial]:
            self.edges[initial][terminal] = weight
        if not initial in self.edgesOptions:
            self.edgesOptions[initial] = {}
        if not terminal in self.edgesOptions[initial]:
            self.edgesOptions[initial][terminal] = tikzOptions

    def isEdge(self, initial, terminal):
        """
        Checks whether an edge with the given initial and terminal vertex is
        already present in the graph.

        Args:
            initial (str): the initial vertex of the seeked edge
            terminal (str): the terminal vertex of the seeked edge

        Returns:
            bool: `True` if the given edge is present in the graph; `False` otherwise.
        """
        return initial in self.edges and terminal in self.edges[initial]

    def getEdgeWeight(self, initial, terminal):
        """
        Args:
            initial (str): the initial vertex of the edge
            terminal (str): the terminal vertex of the edge

        Returns:
            float: the weight of the edge;
            returns `None` if the give edge is not present in the graph
        """
        if self.isEdge(initial, terminal):
            return self.edges[initial][terminal]
        else:
            return None

    def getEdgeOptions(self, initial, terminal):
        """
        Args:
            initial (str): the initial vertex of the edge
            terminal (str): the terminal vertex of the edge

        Returns:
            str: additional options determining how the edge will be drawn by
                TikZ;
            returns empty string if the TikZ options are not specified for this
                edge
        """
        if initial in self.edgesOptions and terminal in self.edgesOptions[initial]:
            return self.edgesOptions[initial][terminal]
        else:
            return ""

    def show(self):
        """
        Prints the values of the attributes of this instance to the terminal
        output.

        Serves mainly to debugging purposes.
        """
        print("vertices:", self.vertices)
        print("edges:", self.edges)
        print("edgesOptions:", self.edgesOptions)

    # ========================================================================================
    # TikZ
    # ========================================================================================

    def exportHeadToTikZ(
            self,
            includeTikZDefinitions = True,
            indent = "",
            indentTab = "    "):
        """
        Args:
            includeTikZDefinitions (bool, optional): if `True` then the TikZ
                definitions of graph nodes and edges will be included to the head
                of the TikZ image
            indent (str, optional): text written at the beginning of each line
                to perform indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform
                indenting of more nested parts of the resulting LaTeX code
                (by default: string with four spaces)

        Returns:
            str: initial part of the TikZ code to draw this graph
        """
        text = ""
        text += indent + r"\begin{tikzpicture}[scale=2, auto]" + "\n"
        if includeTikZDefinitions:
            text += indent + indentTab + r"\tikzstyle{graph vertex} = [circle,draw=black,fill=white,very thick,inner sep=1.5pt, minimum size=5mm]" + "\n"
            text += indent + indentTab + r"\tikzstyle{graph edge undirected} = [draw=black]" + "\n"
            text += indent + indentTab + r"\tikzstyle{graph edge directed} = [graph edge undirected, ->, >=angle 60]" + "\n"
        return text

    def exportFootToTikZ(
            self,
            indent = "",
            indentTab = "    "):
        """
        Args:
            indent (str, optional): text written at the beginning of each line
                to perform indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform
                indenting of more nested parts of the resulting LaTeX code
                (by default: string with four spaces)

        Returns:
            str: terminal part of the TikZ code to draw this graph
        """
        text = ""
        text += indent + r"\end{tikzpicture}" + "\n"
        return text

    def exportVerticesToTikZ(
            self,
            additionalTikZOptions = "",
            indent = "",
            indentTab = "    "):
        """
        Args:
            additionalTikZOptions (str): additional options determining how the
                edges will be drawn by TikZ
            indent (str, optional): text written at the beginning of each line
                to perform indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform
                indenting of more nested parts of the resulting LaTeX code
                (by default: string with four spaces)

        Returns:
            str: TikZ code to draw the vertices of this graph
        """
        text = ""
        for vertex in self.vertices:
            text += indent
            text += r"\node[graph vertex"
            if additionalTikZOptions != "":
                text += ", "
                text += additionalTikZOptions
            text += r"] (" + str(vertex) + r")"
            text += r" at " + str(self.vertices[vertex])
            text += r" {" + str(vertex) + r"};" + "\n"
        return text

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
        text = ""

        text += indent
        text += r"\draw[" + edgeStyle

        weight = self.getEdgeWeight(initial, terminal)
        tikzOptions = self.getEdgeOptions(initial, terminal)
        if tikzOptions != "":
            text += ", " + tikzOptions
        if additionalTikZOptions != "":
            text += ", " + additionalTikZOptions

        text += r"] (" + str(initial) + r") to"

        if weight != None and showWeight != False:
            text += " node {" + str(weight) + "}"

        text += r" (" + str(terminal) + r");" + "\n"

        return text

    def exportEdgesToTikZ(
            self,
            showWeight = True,
            edgeStyle = "graph edge directed",
            additionalTikZOptions = "",
            indent = "",
            indentTab = "    "):
        """
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
            edgeStyle = "graph edge directed",
            includeTikZDefinitions = True,
            additionalTikZOptionsForVertices = "",
            additionalTikZOptionsForEdges = "",
            indent = "",
            indentTab = "    "):
        """
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
        text = ""
        text += self.exportHeadToTikZ(
                includeTikZDefinitions = includeTikZDefinitions,
                indent = indent,
                indentTab = indentTab)
        text += self.exportVerticesToTikZ(
                additionalTikZOptions = additionalTikZOptionsForVertices,
                indent = indent,
                indentTab = indentTab)
        text += self.exportEdgesToTikZ(
                showWeight = showWeight,
                edgeStyle = edgeStyle,
                additionalTikZOptions = additionalTikZOptionsForEdges,
                indent = indent,
                indentTab = indentTab)
        text += self.exportFootToTikZ(
                indent = indent,
                indentTab = indentTab)
        return text

    # ========================================================================================
    # PSTricks
    # ========================================================================================

    def exportHeadToPSTricks(self):
        """
        Returns:
            str: initial part of a PSTricks code to draw this graph
        """
        lowestXCoordinate = None
        lowestYCoordinate = None
        highestXCoordinate = None
        highestYCoordinate = None

        for vertex in self.vertices:
            if lowestXCoordinate == None or lowestXCoordinate > self.vertices[vertex][0]:
                lowestXCoordinate = self.vertices[vertex][0]
            if lowestYCoordinate == None or lowestYCoordinate > self.vertices[vertex][1]:
                lowestYCoordinate = self.vertices[vertex][1]
            if highestXCoordinate == None or highestXCoordinate > self.vertices[vertex][0]:
                highestXCoordinate = self.vertices[vertex][0]
            if highestYCoordinate == None or highestYCoordinate > self.vertices[vertex][1]:
                highestYCoordinate = self.vertices[vertex][1]

        text = ""
        text += "\\psset{unit=1.0cm}\n"
        text += "\\begin{pspicture}("
        text += lowestXCoordinate
        text += ","
        text += lowestYCoordinate
        text += ")("
        text += highestXCoordinate
        text += ","
        text += highestYCoordinate
        text += ")\n"
        return text

    def exportFootToPSTricks(self):
        """
        Returns:
            str: terminal part of a PSTricks code to draw this graph
        """
        text = ""
        text += "\\end{pspicture}\n"
        return text

    def exportVerticesToPSTricks(self):
        """
        Returns:
            str: PSTricks code to draw the vertices of this graph
        """
        text = ""
        for vertex in self.vertices:
            text += "\\cnodeput("
            text += self.vertices[vertex][0]
            text += ","
            text += self.vertices[vertex][1]
            text += "){"
            text += str(vertex)
            text += "}{"
            text += str(vertex)
            text += "}\n"
        return text

    def exportEdgeToPSTricks(self, initial, terminal):
        """
        Args:
            initial (str): the initial vertex of the edge
            terminal (str): the terminal vertex of the edge

        Returns:
            str: PSTricks code to draw an edge of this graph
        """
        text = ""
        text += "\\ncline{"
        text += str(initial)
        text += "}{"
        text += str(terminal)
        text += "}\n"
        weight = self.getEdgeWeight(initial, terminal)
        if weight != None:
            text += "\\ncput*{" + str(weight) + "}\n"
        return text

    def exportEdgesToPSTricks(self):
        """
        Returns:
            str: PSTricks code to draw the edges of this graph
        """
        text = ""
        for vertex in self.edges:
            for neighbour in self.edges[vertex]:
                if vertex < neighbour:
                    text += self.exportEdgeToPSTricks(vertex, neighbour)
        return text

    def exportToPSTricks(self):
        """
        Returns:
            str: PSTricks code to draw this graph
        """
        text = ""
        text += self.exportHeadToPSTricks()
        text += self.exportVerticesToPSTricks()
        text += self.exportEdgesToPSTricks()
        text += self.exportFootToPSTricks()
        return text

    # ========================================================================================
    # LaTeX
    # ========================================================================================

    def saveToLaTeXFile(self, path):
        """
        Saves a TikZ image of this graph to a LaTeX file.

        Args:
            path (str): path to the LaTeX file
        """
        with open(path, "w") as out:
            out.write(teachmedijkstra.getLaTeXHead())
            out.write(self.exportToTikZ())
            out.write(teachmedijkstra.getLaTeXFoot())

