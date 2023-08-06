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
Definition of class `LineInQuineMcCluskey` which implements a line that
    represents a term, or merged terms, in the first phase of the Quine-McCluskey
    algorithm (when it is finding prime implicants).
"""

__all__ = ["LineInQuineMcCluskey"]

import copy
import string

class LineInQuineMcCluskey:
    """
    Implements a line that represents a term, or merged terms, in the
        first phase of the Quine-McCluskey algorithm (when it is finding prime
        implicants).

    Attributes:
        identifier (list of int): It is a list of non-negative integers which
                denote the original (initial) terms from which this term has been
                created by merging.
            In the beginning, each line (i.e. term) has a unique integer
                assigned.
            Further, when two lines are merged, the identifier of the resulting
                line is the union of the identifiers of the two original lines.
            For example, lines
                [5] (1, 0, 0)
                and
                [7] (1, 1, 0)
                are merged to
                [5, 7] (1, 2, 0).
        term (tuple of int): The integer values in the tuple are from the set
            {0, 1, 2};

            * **0** stands for logical zero ("non-truth"),
            * **1** stands for logical unit ("truth"),
            * **2** stands for undetermined value (if the values of two original
                lines were, on this particular position, both "truth" and
                "non-truth"; see also the example ebove).
        used (bool): Denotes whether this line has been merged with another
                line.
            If it is `False` then the term corresponding to this line may
            appear in the resulting minimized DNF (disjunctive normal form).
        removed (bool): If `True` then this line has been removed from the list
                since another identical line is already present.
            Such a line could be deleted directly, however, this allows to make
                this removed line visible in the resulting LeTeX output.
        undetermined ... text in LaTeX format
            Represents the symbols which is used to denote the undetermined
                (don't care) value in a line of a step of the Quine-McCluskey
                algorithm.
            It corresponds with the value `2` in the description of the
                attribute `term`.
            It is '\\text{-}' by default and it can be changed if another
                symbol is preferred.
    """
    #TODO move undetermined to Constants

    def __init__(self, identifier, term):
        self.identifier = identifier
        self.term = term
        self.used = False
        self.removed = False
        self.undetermined = r'\text{-}'

    def __str__(self):
        return self.exportToText()

    def canBeMergedWith(self, other):
        """
        Checks whether this line can be merged with the given line.

        Args:
            other (LineInQuineMcCluskey): reference to the line that shall be
                merged with this one

        Returns:
            int: Returns `-1` if the two lines cannot be merged,
                or a non-negative integer which represents the index of the
                (single) position where the terms of the two lines differ
                (and where the term of the resulting line shall have
                the `undetermined` value)
        """
        l = len(self.term)
        if l != len(other.term):
            return None
        result = None
        for i in range(l):
            if self.term[i] != other.term[i]:
                if result == None:
                    result = i
                else:
                    return None
        return result

    def mergeWith(self, other):
        """
        Merges this line with the given line provided that the merge is
            possible.

        If the merge has been performed, the attribute `used` is set to `True`
            in both original lines.

        Args:
            other (LineInQuineMcCluskey): reference to the line that shall be
                merged with this one

        Returns:
            LineInQuineMcCluskey: Returns `None` if the two lines cannot be
                merged, or the reference to the resulting (merged) line.
        """
        where = self.canBeMergedWith(other)
        if where != None:
            newIdentifier = copy.copy(self.identifier)
            newIdentifier.extend(other.identifier)
            newTerm = list(self.term)
            newTerm[where] = 2
            new = LineInQuineMcCluskey(newIdentifier, tuple(newTerm))
            self.used = True
            other.used = True
            return new
        else:
            return None

    def getConjunctionLength(self, withConjunctions = True, withNegations = True):
        """
        Returns the length in characters (symbols) of the conjunction that
            represents this term.

        Args:
            withConjunctions (bool, optional): if `True` then each conjunction
                symbol increase the returned value by one;
            withNegations (bool, optional): if `True` then each negation symbol
                increase the returned value by one

        Example:
            The length of the conjunction a'bc is:

            * 3 ... if `withConjunctions == False` and `withNegations == False`
            * 4 ... if `withConjunctions == False` and `withNegations == True `
            * 5 ... if `withConjunctions == True ` and `withNegations == False`
            * 6 ... if `withConjunctions == True ` and `withNegations == True `
        """
        result = 0
        first = True
        for literal in self.term:
            if first:
                first = False
            else:
                if withConjunctions:
                    result += 1
            if literal == 0:
                if withNegations:
                    result += 2
                else:
                    result += 1
            elif literal == 1:
                result += 1
        return result

    def exportConjunctionToLaTeX(self,
            textAnd = "\\land",
            letters = None):
        """
        Args:
            textAnd (str, optional): LaTeX macro for conjunction
                (by default: `\\land`)
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')

        Returns:
            str: string with LaTeX conjunction representing the conjunction
                given by the term if this line
        """
        if letters == None:
            letters = list(string.ascii_lowercase)
        text = ""
        first = True
        for i in range(len(self.term)):
            literal = self.term[i]
            if literal in [0,1]:
                if first:
                    first = False
                else:
                    if textAnd != "":
                        text += "{" + textAnd + "}"
                text += letters[i]
                if literal == 0:
                    text += "'"
        if first:
            text += "1"
        return text

    def exportConjunctionToText(self, letters = None):
        """
        Args:
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')

        Returns:
            str: string representing the conjunction given by the term if this
                line
        """
        if letters == None:
            letters = list(string.ascii_lowercase)
        text = ""
        tautology = True
        for i in range(len(self.term)):
            literal = self.term[i]
            if literal in [0,1]:
                text += letters[i]
                if literal == 0:
                    text += "'"
                tautology = False
        if tautology:
            return "1"
        else:
            return text

    def exportIdentifierToLaTeX(self):
        """
        Returns:
            str: LaTeX code representing the identifier of this line
        """
        text = ""
        for i in range(len(self.identifier)):
            if i > 0:
                text += ","
            text += str(self.identifier[i])
        return text

    def exportIdentifierToText(self):
        """
        Returns:
            str: string representing the identifier of this line
        """
        text = ""
        for i in range(len(self.identifier)):
            if i > 0:
                text += ","
            text += str(self.identifier[i])
        return text

    def exportTermToLaTeXTableHeader(self):
        """
        Returns this line as a term in LaTeX code which is suitable to be used
            in the header of a LaTeX table.

        Supposedly, this shall be used to write the covering matrix of the
            Quine-McCluskey algorithm.

        Returns:
            str: LaTeX code representing the term of this line
        """
        text = ""
        first = True
        for literal in self.term:
            if first:
                first = False
            else:
                text += r" {\;} "
            if literal in [0,1]:
                text += str(literal)
            else:
                text += self.undetermined
        return text

    def exportTermToLaTeXTable(self):
        """
        Returns this line as a term in LaTeX code which is suitable to be used
            in the leftmost column of a LaTeX table.

        Supposedly, this shall be used to write the covering matrix of the
            Quine-McCluskey algorithm.

        Returns:
            str: LaTeX code representing the term of this line
        """
        text = ""
        first = True
        for literal in self.term:
            if first:
                first = False
            else:
                text += " & "
            if literal in [0,1]:
                text += str(literal)
            else:
                text += self.undetermined
        return text

    def exportToLaTeX(self, indent = ""):
        """
        Serves to export one step of the first phase of the Quine-McCluskey
            algorithm (when finding the prime implicants).

        Such a step consists of several lines with identifiers with (possibly
            merged) terms and it is exported as a LaTeX table.
        Therefore the output of this method is actually a line of a LaTeX
            table.

        Args:
            indent (str, optional): text written at the beginning of each line to perform
                indenting of the LaTeX code
                (by default: empty string)

        Returns:
            str: LaTeX code representing this line
        """
        text = ""
        text += indent
        if self.removed:
            text += "\\removed{"
        text += self.exportIdentifierToLaTeX()
        text += ":"
        if self.removed:
            text += "}"
        text += " & "
        first = True
        for literal in self.term:
            if first:
                first = False
            else:
                text += " & "
            if self.removed:
                text += "\\removed{"
            if literal in [0,1]:
                text += str(literal)
            else:
                text += self.undetermined
            if self.removed:
                text += "}"
        text += " & "
        if self.used:
            text += "\\checkmark"
        #text += "\\\\\n"
        return text

    def exportTermToText(self):
        """
        Returns:
            str: string representing the term of this line; it is a sequence of
                the characters '0', '1', and '-'
        """
        text = ""

        for literal in self.term:
            if literal in [0,1]:
                text += str(literal)
            elif literal == 2:
                text += "-"
            else:
                text += "?"
        return text

    def exportToText(self):
        """
        Returns:
            str: string representing this line
        """
        text = ""
        text += self.exportIdentifierToText()
        text += " "
        text += self.exportTermToText()
        text += " "
        if self.used:
            text += "U"
        else:
            text += "."
        text += " "
        if self.removed:
            text += "R"
        else:
            text += "."
        return text

