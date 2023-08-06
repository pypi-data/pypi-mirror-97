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
Definition of class `Dijkstra` which implements the Dijkstra's algorithm for
finding the shortest paths in a directed or undirected graph.
"""

import copy
import teachmedijkstra

class Dijkstra:
    """
    Implements the Dijkstra's algorithm for finding the shortest paths in a
    directed or undirected graph.

    Apart from the computation of the shortest paths, the class is also able to
    export the shortest path tree (shortest path covering) as a TikZ image and
    to export, in a LaTeX table, the values assigned to the graph vertices in
    each individual step of the algorithm.

    Attributes:
        graph (teachmedijkstra.DirectedGraph or teachmedijkstra.UndirectedGraph): the processed graph
        startingVertex (str): the name of the vertex from which the shortest
            paths are to be found
        table (dict of list of dict): contains the data to export the LaTeX table
            with the information about the progress of the algorithm run;
            see `Dijkstra.exportTableToLaTeX`.
            One dimension of the table corresponds to the vertices of the graph
            and the second one corresponds to the time steps of the algorithm
            run.
            The keys of the `dict` are names of the vertices of the processed
            graph and the values are `list` of time steps.
            Each item in the list is a `dict` with the keys:

            * `"predecessor"`: predecessor of the vertex on the shortest path
                found so far
            * `"distance"`: length of the shortest path found so far
            * `"closed"`: `True` if all the successors of the vertex have
                already been visited
            * `"overwritten"`: `True` if `distance` has been overwritten in
                this step

        closed (dict of bool): The keys are the names of the vertices of the
            processed graph and the values are either `True` or `False` indicating
            whether the vertex has been already processed by the algorithm
        numOverwrites (int): how many times (totally, during the algorithm run)
            has been the value `distance` of a vertex overwritten by a smaller
            value;
            If graphs are randomly generated for a purpose of examen tests,
            this can serve as an indicator of the complexity of the test.
        maxOverwrites (int): the maximal possible value of `numOverwrites`;
            computed according to the number of the vertices and the number of
            the edges of the graph
        shortestPathTree (set of 2-tuples): set of pairs of vertices describing
            the edges that belong to the shortest path tree (shortest path
            covering)
    """
    def __init__(self, graph, startingVertex):
        self.graph = graph
        self.startingVertex = startingVertex
        self.table = {}
        self.closed = {}
        self.numOverwrites = 0
        self.maxOverwrites = self.graph.getNumberOfEdges() - self.graph.getNumberOfVertices() + 1
        self.shortestPathTree = set([])
        for vertex in self.graph.vertices.keys():
            self.table[vertex] = []
            self.closed[vertex] = False
            if vertex == self.startingVertex:
                self.table[vertex].append({"predecessor": None, "distance": 0, "closed": False, "overwritten": False})
            else:
                self.table[vertex].append({"predecessor": None, "distance": None, "closed": False, "overwritten": False})
        self.numSteps = 1

    def run(self):
        """
        Performs the Dijkstra's algorithm.
        """
        for i in range(len(self.table)):
            vertexMin = None
            vertexMinDistance = None
            for vertex in self.table.keys():
                if not self.closed[vertex] and self.table[vertex][i]["distance"] != None:
                    if vertexMin == None or (self.table[vertex][i]["distance"] != None and self.table[vertex][i]["distance"] < vertexMinDistance):
                        vertexMin = vertex
                        vertexMinDistance = self.table[vertex][i]["distance"]
            self.closed[vertexMin] = True
            if self.table[vertexMin][i]["predecessor"] != None:
                self.shortestPathTree.add((vertexMin, self.table[vertexMin][i]["predecessor"]))
                self.shortestPathTree.add((self.table[vertexMin][i]["predecessor"], vertexMin))
            if i + 1 < len(self.table):
                for vertex in self.table.keys():
                    self.table[vertex].append(copy.deepcopy(self.table[vertex][i]))
                    self.table[vertex][i + 1]["overwritten"] = False
                self.table[vertexMin][i + 1] = {"predecessor": vertexMin, "distance": vertexMinDistance, "closed": True, "overwritten": False}
                for neighbour in self.graph.edges[vertexMin].keys():
                    if not self.closed[neighbour]:
                        neighbourDistance = self.graph.edges[vertexMin][neighbour]
                        newDistance = vertexMinDistance + neighbourDistance
                        if self.table[neighbour][i + 1] == {"predecessor": None, "distance": None, "closed": False, "overwritten": False}:
                            self.table[neighbour][i + 1] = {"predecessor": vertexMin, "distance": newDistance, "closed": False, "overwritten": False}
                        elif self.table[neighbour][i + 1]["distance"] > newDistance:
                            self.numOverwrites += 1
                            self.table[neighbour][i + 1] = {"predecessor": vertexMin, "distance": newDistance, "closed": False, "overwritten": True}
                self.numSteps += 1

    def exportTableToLaTeX(self, indent = ""):
        """
        Returns:
            str: the content of the attribute `table` formattes to a LaTeX
                table
        """
        text = ""
        text += "\\begin{tabular}{"
        text += "|r||"
        for i in range(1, self.numSteps+1, 1):
            text += "c@{\\,}c|"
        text += "}\n"
        text += "\\hline\n"
        for i in range(1, self.numSteps+1, 1):
            text += " & & " + str(i) + "."
        text += "\\\\\n"
        text += "\\hline\n"
        for vertex in sorted(self.table):
            text += str(vertex)
            for step in self.table[vertex]:
                if not step["closed"]:
                    text += " & "
                    if step["predecessor"] == None:
                        text += "$\\cdot$"
                    else:
                        if step["overwritten"]:
                            text += "\\textbf{"
                        text += str(step["predecessor"])
                        if step["overwritten"]:
                            text += "}"
                    text += " & "
                    if step["distance"] == None:
                        text += "$\\infty$"
                    else:
                        if step["overwritten"]:
                            text += "\\textbf{"
                        text += str(step["distance"])
                        if step["overwritten"]:
                            text += "}"
                else:
                    text += " & & "
            text += "\\\\\n"
            text += "\\hline\n"
        text += "\\end{tabular}\n"
        return text

    def exportShortestPathTreeToTikZ(
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
            str: TikZ image describing the shortest path tree (shortest path covering)
        """
        text = ""
        text += self.graph.exportHeadToTikZ(includeTikZDefinitions = includeTikZDefinitions)
        text += self.graph.exportVerticesToTikZ()
        for vertex in self.graph.edges:
            for neighbour in self.graph.edges[vertex]:
                if self.graph.__class__.__name__ == "DirectedGraph" or vertex < neighbour:
                    if (vertex, neighbour) in self.shortestPathTree:
                        text += self.graph.exportEdgeToTikZ(vertex, neighbour, showWeight = False, additionalTikZOptions = "ultra thick")
                    else:
                        text += self.graph.exportEdgeToTikZ(vertex, neighbour, showWeight = False, additionalTikZOptions = "very thin, gray")
        text += self.graph.exportFootToTikZ()
        return text

    def exportTableToText(self):
        """
        Returns:
            str: the content of the attribute `table` as a plain text table
        """
        text = ""
        for vertex in self.table.keys():
            text += str(vertex)
            if self.closed[vertex]:
                text += "*"
            else:
                text += " "
            text += ": | "
            for i in self.table[vertex]:
                if not i["closed"]:
                    if i["predecessor"] == None:
                        text += "."
                    else:
                        text += str(i["predecessor"])
                    text += " "
                    if i["distance"] == None:
                        text += "inf"
                    else:
                        if i["distance"] < 10:
                            text += " "
                        if i["distance"] < 100:
                            text += " "
                        text += str(i["distance"])
                else:
                    text += "     "
                text += " | "
            text += "\n"
        return text

    def saveToLaTeXFile(self, path):
        """
        Exports the graph, the table describing the progress of the algorithm, and
        the shortest path tree to a LaTeX file.

        Args:
            path (str): path to the LaTeX file
        """
        with open(path, "w") as out:
            out.write(teachmedijkstra.getLaTeXHead())
            out.write(r"\begin{center}" + "\n")
            out.write(self.graph.exportToTikZ())
            out.write(r"\end{center}" + "\n")
            out.write(r"\begin{center}" + "\n")
            out.write(self.exportTableToLaTeX())
            out.write(r"\end{center}" + "\n")
            out.write(r"\begin{center}" + "\n")
            out.write(self.exportShortestPathTreeToTikZ())
            out.write(r"\end{center}" + "\n")
            out.write(teachmedijkstra.getLaTeXFoot())

    def show(self):
        """
        Prints the content of the attribute `table` and of some other
        attributes to the terminal output.

        This method serves mainly for debugging purposes.

        Call this method **after** calling the method `Dijkstra.run`.
        """
        print(self.exportTableToText())
        print("numVertices:", self.graph.getNumberOfVertices())
        print("numEdges:", self.graph.getNumberOfEdges())
        print("numOverwrites:", self.numOverwrites)
        print("maxOverwrites:", self.maxOverwrites)
        print("shortestPathTree:", self.shortestPathTree)

