# -*- coding: UTF-8 -*-

# This file is a part of teachmeqmc which is a Python3 package designed for
# educational purposes to demonstrate the Quine-McCluskey algorithm.
#
# Copyright (c) 2021 Milan Petrík <milan.petrik@protonmail.com>
#
# Web page of the program: <https://gitlab.com/petrikm/teachmeqmc>
#
# teachmeqmc is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# teachmeqmc is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# teachmeqmc. If not, see <https://www.gnu.org/licenses/>.

"""
    Various utility functions.
"""

__all__ = ["generateGrayCode", "getLaTeXHead", "getLaTeXFoot"]

import datetime

from teachmeqmc.Constants import *

def generateGrayCode(numInputs):
    """
    Generates the Gray code of a given word length.

    Gray code is a sequence of binary words of a specified length such that two
        consequent words differ in a single bit.

    Example:
        Gray code of word length 3 is:

            0 0 0
            0 0 1
            0 1 1
            0 1 0
            1 1 0
            1 1 1
            1 0 1
            1 0 0

    Args:
        numInputs (int): length of the words that form the desired Gray code

    Returns:
        list of tuples: Length of each tuple is equal to `numInputs`.
            The tuples contain `0` and `1` and successively describe the
                desired Gray code.
            If the code cannot be created (e.g. if `numInputs` is zero), `None`
                is returned.

    See:
        Utilized by `exportAsKarnaughMapToTikZ` of `teachmeqmc.BooleanFunction`
    """
    if numInputs == 1:
        return [(0,), (1,)]
    elif numInputs > 1:
        smaller = generateGrayCode(numInputs - 1)
        zeroList = []
        unitList = []
        l = len(smaller)
        for i in range(l):
            zeroList.append((0,) + smaller[i])
            unitList.append((1,) + smaller[l - i - 1])
        return zeroList + unitList
    else:
        return None

def getLaTeXHead():
    """Returns the initial part of a LaTeX file which is suitable to be used
        with `exportToLaTeX` of `teachmeqmc.BooleanFunction`.

    Example:
        Having an instance `b` of `teachmeqmc.BooleanFunction`, the complete
            output LaTeX file can be written by:

            with open(path, "w") as out:
                out.write(getLaTeXHead())
                out.write(b.exportToLaTeX())
                out.write(getLaTeXFoot())

    Returns:
        str: LaTeX code containing initial part of a LaTeX document

    See:
        Utilized by `saveToLaTeX` of `teachmeqmc.BooleanFunction`
    """
    text = ""
    text += r'% This file has been generated automatically by teachmeqmc ' + __version__ + "\n"
    text += r'% Time of the creation: ' + str(datetime.datetime.now()) + "\n"
    text += "\n"
    text += r'% teachmeqmc is a Python3 package' + "\n"
    text += r'% web page: https://gitlab.com/petrikm/teachmeqmc' + "\n"
    text += r'% author: Milan Petrík' + "\n"
    text += r'% e-mail: milan.petrik@protonmail.com' + "\n"
    text += "\n"
    text += r'\documentclass{article}' + "\n"
    text += "\n"
    text += r'% Import TikZ for drawing Karnaugh maps of the processed Boolean functions' + "\n"
    text += r'\usepackage{tikz}' + "\n"
    text += r'% Import AMS packages for: \text, \checkmark, and align environment' + "\n"
    text += r'\usepackage{amsmath,amssymb}' + "\n"
    text += r'% To have a clickable reference to the web page of teachmeqmc' + "\n"
    text += r'\usepackage{hyperref}' + "\n"
    text += "\n"
    text += r'% Macro for denoting the redundant (duplicate) rows which may occur' + "\n"
    text += r'% during the first phase of the Quine-McCluskey algorithm' + "\n"
    text += r'\definecolor{gray}{rgb}{0.75,0.75,0.75}' + "\n"
    text += r'\newcommand{\removed}[1]{\textcolor{gray}{#1}}' + "\n"
    text += "\n"
    text += r'\begin{document}' + "\n"
    text += "\n"
    text += r'\begin{center}' + "\n"
    text += r'    {\LARGE Quine-McCluskey algorithm\footnote{' + "\n"
    text += r'    This file has been generated automatically by \texttt{teachmeqmc-' + __version__ + "}\n"
    text += r'    which is a Python3 package' + "\n"
    text += r'    available at \url{https://gitlab.com/petrikm/teachmeqmc}.' + "\n"
    text += r'    }}' + "\n"
    text += r'\end{center}' + "\n"
    text += "\n"
    return text

def getLaTeXFoot():
    """Returns the terminal part of a LaTeX file which is suitable to be used
        with `exportToLaTeX` of `teachmeqmc.BooleanFunction`.

    Example:
        Having an instance `b` of `teachmeqmc.BooleanFunction`, the complete
            output LaTeX file can be written by:

            with open(path, "w") as out:
                out.write(getLaTeXHead())
                out.write(b.exportToLaTeX())
                out.write(getLaTeXFoot())

    Returns:
        str: LaTeX code containing terminal part of a LaTeX document

    See:
        Utilized by `saveToLaTeX` of `teachmeqmc.BooleanFunction`
    """
    text = ""
    text += r'\end{document}' + "\n"
    return text

