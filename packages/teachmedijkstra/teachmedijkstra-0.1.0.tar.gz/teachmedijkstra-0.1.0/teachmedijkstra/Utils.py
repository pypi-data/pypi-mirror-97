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
    Various utility functions.
"""

__all__ = ["getLaTeXHead", "getLaTeXFoot"]

import datetime

import teachmedijkstra.Constants

def getLaTeXHead():
    """Returns the initial part of a LaTeX file which is suitable to be used
        with `export...ToLaTeX` methods of `teachmedijkstra.Dijkstra`.

    Example:
        Having an instance `d` of `teachmedijkstra.Dijkstra`, the complete
            output LaTeX file can be written by:

            with open(path, "w") as out:
                out.write(getLaTeXHead())
                out.write(d.exportToLaTeX())
                out.write(getLaTeXFoot())

    Returns:
        str: LaTeX code containing initial part of a LaTeX document

    See:
        Utilized by `saveToLaTeX` of `teachmedijkstra.Dijkstra`
    """
    text = ""
    text += r"% This file has been generated automatically by teachmedijkstra " + teachmedijkstra.Constants.__version__ + "\n"
    text += r"% Time of the creation: " + str(datetime.datetime.now()) + "\n"
    text += "\n"
    text += r"% teachmedijkstra is a Python3 package" + "\n"
    text += r"% web page: https://gitlab.com/petrikm/teachmedijkstra" + "\n"
    text += r"% author: Milan Petrík" + "\n"
    text += r"% e-mail: milan.petrik@protonmail.com" + "\n"
    text += "\n"
    text += r"\documentclass{article}" + "\n"
    text += "\n"
    text += r"% Import TikZ to draw the graph and the shortest path tree" + "\n"
    text += r"\usepackage{tikz}" + "\n"
    text += r"% TikZ library to depict the edges of a directed graph as arrows" + "\n"
    text += r"\usetikzlibrary{arrows}" + "\n"
    text += r"% To have a clickable reference to the web page of teachmedijkstra" + "\n"
    text += r"\usepackage{hyperref}" + "\n"
    text += "\n"
    text += r"\begin{document}" + "\n"
    text += "\n"
    text += r"\begin{center}" + "\n"
    text += r"    {\LARGE Dijkstra's algorithm\footnote{" + "\n"
    text += r"    This document has been generated automatically by \texttt{teachmedijkstra-" + teachmedijkstra.Constants.__version__ + "}\n"
    text += r"    which is a Python3 package" + "\n"
    text += r"    available at \url{https://gitlab.com/petrikm/teachmedijkstra}." + "\n"
    text += r"    }}" + "\n"
    text += r"\end{center}" + "\n"
    text += "\n"
    return text

def getLaTeXFoot():
    """Returns the terminal part of a LaTeX file which is suitable to be used
        with `export...ToLaTeX` methods of `teachmedijkstra.Dijkstra`.

    Returns:
        str: LaTeX code containing terminal part of a LaTeX document

    See:
        Utilized by `saveToLaTeX` of `teachmedijkstra.Dijkstra`
    """
    text = ""
    text += r"\end{document}" + "\n"
    return text

