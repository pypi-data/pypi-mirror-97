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
Definition of class `CoveringMatrix` which implements the covering matrix in
    the second phase of the Quine-McCluskey algorithm.
"""

__all__ = ["CoveringMatrix"]

import copy
import string

from teachmeqmc.LineInQuineMcCluskey import *

class CoveringMatrix:
    """
    Implements the covering matrix in the Quine-McCluskey algorithm.

    Corresponds with the second phase of the Quine-McCluskey algorithm when we
        are looking for the smallest subset of the prime implicants (final terms)
        that cover all the initial terms.

    Note that DNF stands for "Disjunctive Normal Form" of a Boolean function.

    Attributes:
        initialLines (list of teachmeqmc.LineInQuineMcCluskey): the lines (terms) that
            belong to the complete DNF
        primeImpLines (list of teachmeqmc.LineInQuineMcCluskey): prime implicants (final
            terms) that have been obtained by (multiple) merging of the initial
            terms during the first phase of the Quine-McCluskey algorithm
        numInputs (int): maximal number of variables (inputs) that may appear
            in a term (number of inputs of the processed Boolean function)
        comment (str): a comment to this particular instance of covering matrix;
            The following values of the attribute `comment` are recognized by
                the class `BooleanFunction`:

            * `"essential"` ... if essential prime implicants were removed from
                this covering matrix
            * `"prime"` ... if some prime implicants were removed from this
                covering matrix (when removing those columns that are a
                subset of another column)
            * `"initial"` ... if some initial terms were removed from this
                covering matrix (when removing those rows that are a
                superset of another row)
    """

    def __init__(self,
            initialLines = None,
            primeImpLines = None,
            parentCoveringMatrix = None,
            numInputs = None,
            comment = ""):
        """
        Either both `initialLines` and `primeImpLines` must be set
            or `parentCoveringMatrix` must be set.

        If `initialLines` and `primeImpLines` are set than the covering matrix
            is created to match the covering that is already given by
            `primeImpLines` themselves.
        (Each element of `primeImpLines` (which is an instance of
            `teachmeqmc.LineInQuineMcCluskey`) already has references to `initialLines` that
            it covers in the attribute `identifier`).

        If `parentCoveringMatrix` is set then this instance will be a deep copy
            of the instance given by the parameter `parentCoveringMatrix`.
        (`parentCoveringMatrix` is an instance of `CoveringMatrix`)
        """
        if parentCoveringMatrix != None:
            self.initialLines = copy.deepcopy(parentCoveringMatrix.initialLines)
            self.primeImpLines = copy.deepcopy(parentCoveringMatrix.primeImpLines)
        elif initialLines != None and primeImpLines != None:
            self.initialLines = copy.deepcopy(initialLines)
            self.primeImpLines = copy.deepcopy(primeImpLines)
        self.numInputs = numInputs
        self.comment = comment

    def removeRedundantInitialLines(self):
        """
        Removes those initial lines that are marked as removed.

        In `initialLines` there are lines (instances of
            `teachmeqmc.LineInQuineMcCluskey`)
            copied from the very first step of the first phase of the
            Quine-McCluskey algorithm (the phase when finding prime
            implicants).
        It is allowed to have duplicate lines there.
        These are, however, already marked as 'removed' by the preceeding steps
            of the algorithm.
        As these duplicates are not needed now, they are deleted by this method.

        Returns nothing, only affects this instance.
        """
        removed = []
        for i in range(len(self.initialLines)):
            if self.initialLines[i].removed:
                removed.append(self.initialLines[i])
        for line in set(removed):
            self.initialLines.remove(line)

    def findAndRemoveEssentialPrimeImplicants(self):
        """
        Finds, removes, and returns a list of essential prime implicants in
            this covering matrix.

        Returns:
            list of teachmeqmc.LineInQuineMcCluskey: list of currently found
                essential prime implicants
        """
        result = []
        removedInitials = len(self.initialLines) * [False]
        removedFinals = len(self.primeImpLines) * [False]
        for initial in self.initialLines:
            numMatches = 0
            matching = None
            for i in range(len(self.primeImpLines)):
                prime = self.primeImpLines[i]
                if set(initial.identifier) <= set(prime.identifier):
                    numMatches += 1
                    matching = i
            if numMatches == 1:
                removedFinals[matching] = True
                pass
        for i in range(len(self.primeImpLines) - 1, -1, -1):
            if removedFinals[i]:
                result.append(self.primeImpLines.pop(i))
        for prime in result:
            for i in range(len(self.initialLines) - 1, -1, -1):
                initial = self.initialLines[i]
                if set(initial.identifier) <= set(prime.identifier):
                    self.initialLines.pop(i)
        return result

    def findAndRemovePrimeImpLinesThatAreSubsets(self):
        """
        Finds and removes those covering matrix columns (i.e. prime implicants)
            that are subsets of another covering matrix column.

        Returns:
            bool: `True` if such columns have been found; `False` otherwise
        """
        anythingChanged = False
        numPrimeImpLines = len(self.primeImpLines)
        subset = numPrimeImpLines * [None]
        for i in range(numPrimeImpLines):
            subset[i] = numPrimeImpLines * [True]
        for initial in self.initialLines:
            for i1 in range(len(self.primeImpLines)):
                final1 = self.primeImpLines[i1]
                for i2 in range(len(self.primeImpLines)):
                    final2 = self.primeImpLines[i2]
                    if set(initial.identifier) <= set(final1.identifier) and not set(initial.identifier) <= set(final2.identifier):
                        # the first one covers
                        subset[i1][i2] = False
                    elif not set(initial.identifier) <= set(final1.identifier) and set(initial.identifier) <= set(final2.identifier):
                        # the second one covers
                        subset[i2][i1] = False
        removed = []
        for i1 in range(len(self.primeImpLines)):
            for i2 in range(i1, len(self.primeImpLines)):
                if i1 != i2:
                    if subset[i1][i2] and not subset[i2][i1]:
                        removed.append(self.primeImpLines[i1])
                        anythingChanged = True
                    if subset[i2][i1] and not subset[i1][i2]:
                        removed.append(self.primeImpLines[i2])
                        anythingChanged = True
        for line in set(removed):
            self.primeImpLines.remove(line)
        return anythingChanged

    def findAndRemoveInitialLinesThatAreSupersets(self):
        """
        Finds and removes those covering matrix rows (initial terms) that are
            supersets of another row.

        Returns:
            bool: `True` if such rows have been found; `False` otherwise
        """
        anythingChanged = False
        numInitialLines = len(self.initialLines)
        superset = numInitialLines * [None]
        for i in range(numInitialLines):
            superset[i] = numInitialLines * [True]
        for prime in self.primeImpLines:
            for i1 in range(len(self.initialLines)):
                initial1 = self.initialLines[i1]
                for i2 in range(len(self.initialLines)):
                    initial2 = self.initialLines[i2]
                    if set(initial1.identifier) <= set(prime.identifier) and not set(initial2.identifier) <= set(prime.identifier):
                        # the first one is covered
                        superset[i2][i1] = False
                    elif not set(initial1.identifier) <= set(prime.identifier) and set(initial2.identifier) <= set(prime.identifier):
                        # the second one is covered
                        superset[i1][i2] = False
        removed = []
        for i1 in range(len(self.initialLines)):
            for i2 in range(i1, len(self.initialLines)):
                if i1 != i2:
                    if superset[i1][i2] and not superset[i2][i1]:
                        removed.append(self.initialLines[i1])
                        anythingChanged = True
                    if superset[i2][i1] and not superset[i1][i2]:
                        removed.append(self.initialLines[i2])
                        anythingChanged = True
        for line in set(removed):
            self.initialLines.remove(line)
        return anythingChanged

    def isCovering(self, primeImpLinesMask):
        """
        Checks whether the selected terms cover all the initial terms.

        This is an auxiliary method for `CoveringMatrix.getResultsByBruteForce`.

        Args:
            primeImpLinesMask (list of bool) ... selection from the prime
                implicants;
                It is a list of the same size as `self.primeImpLines`; it
                contains values `True` or `False` depending on the fact whether
                the given prime implicant belong to the selection, or not.

        Returns:
            bool: `True` if the selected terms cover all the initial terms;
            `False` otherwise
        """
        initialLinesCovered = len(self.initialLines) * [False]
        for f in range(len(self.primeImpLines)):
            prime = self.primeImpLines[f]
            if primeImpLinesMask[f]:
                for i in range(len(self.initialLines)):
                    initial = self.initialLines[i]
                    if set(initial.identifier) <= set(prime.identifier):
                        initialLinesCovered[i] = True
        for covered in initialLinesCovered:
            if not covered:
                return False
        return True

    def getResultsByBruteForce(self):
        """
        Finds all the minimal coverings (all the minimal DNFs) by a brute force
            method.

        Brute force method = try all the possible subsets and choose the
            smallest ones.

        When the covering matrix cannot be simplified any further (by finding
            the essential prime implicants, by removing those columns that are
            a subset of another column, or by removing those rows that are a
            superset of another row) then the brute-force is applied.

        Returns:
            list of lists of teachmeqmc.LineInQuineMcCluskey: the list of minimal DNFs
        """
        results = []
        # find all the subsets of prime implicants that cover the initial terms
        primeImpLinesMask = len(self.primeImpLines) * [False]
        while True:
            for i in range(len(primeImpLinesMask)):
                if primeImpLinesMask[i] == False:
                    primeImpLinesMask[i] = True
                    break
                else:
                    primeImpLinesMask[i] = False
            terminate = True
            for i in range(len(primeImpLinesMask)):
                if primeImpLinesMask[i] == True:
                    terminate = False
                    break
            if terminate:
                break
            if self.isCovering(primeImpLinesMask):
                dnf = []
                for i in range(len(primeImpLinesMask)):
                    if primeImpLinesMask[i]:
                        dnf.append(self.primeImpLines[i])
                results.append(dnf)
        # find the size (in number of terms) of the smallest resulting DNF
        minLength = None
        for dnf in results:
            if minLength == None or minLength > len(dnf):
                minLength = len(dnf)
        # remove those subsets of prime implicants that have a greater size than `minLength`
        for i in range(len(results) - 1, -1, -1):
            dnf = results[i]
            if len(dnf) > minLength:
                results.pop(i)
        return results

    def isEmpty(self):
        """
        Checks whether this covering matrix is empty.

        The covering matrix is empty

         * if the number of its columns is zero,
         * or if the number of its rows is zero.

        Returns:
            bool: `True` if it is empty; `False` otherwise
        """
        return len(self.initialLines) == 0 or len(self.primeImpLines) == 0

    def exportToLaTeX(self,
            textAnd = "\\land",
            letters = None,
            indent = "",
            indentTab = "    "):
        """
        Serves to export this covering matrix as a table in LaTeX.

        The table is written using the LaTeX environment `{array}`.

        Args:
            textAnd (str, optional): LaTeX macro for conjunction
                (by default: `\\land`)
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')
            indent (str, optional): text written at the beginning of each line to perform
                indenting of the LaTeX code
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform indenting of
                more nested parts of the resulting LaTeX code
                (by default: string with four spaces)

        Returns:
            str: LaTeX code describing this covering table
        """
        if letters == None:
            letters = list(string.ascii_lowercase)
        text = indent + "\\begin{array}{|r|"
        first = True
        for i in range(self.numInputs):
            if first:
                first = False
            else:
                text += "@{\\;}"
            text += "c"
        text += "|c||"
        for i in range(len(self.primeImpLines)):
            text += "c|"
        text += "}\n"
        text += indent + indentTab + "\\hline\n"
        # first row of the covering matrix (identifiers of the prime implicants)
        text += indent + indentTab
        for i in range(self.numInputs):
            text += " & "
        text += " & "
        for prime in self.primeImpLines:
            text += " & "
            text += prime.exportIdentifierToLaTeX()
        text += "\\\\\n"
        text += indent + indentTab + "\\hline\n"
        # second row of the covering matrix (representations of the prime implicants)
        text += indent + indentTab
        for i in range(self.numInputs):
            text += " & "
        text += " & "
        for prime in self.primeImpLines:
            text += " & "
            text += prime.exportTermToLaTeXTableHeader()
        text += "\\\\\n"
        text += indent + indentTab + "\\hline\n"
        # third row of the covering matrix (prime implicants written as formulas)
        text += indent + indentTab
        for i in range(self.numInputs):
            text += " & "
        text += " & "
        for prime in self.primeImpLines:
            text += " & "
            text += prime.exportConjunctionToLaTeX(textAnd = textAnd, letters = letters)
        text += "\\\\\n"
        text += indent + indentTab + "\\hline\n"
        if len(self.initialLines) > 0:
            text += indent + indentTab + "\\hline\n"
        # the covering matrix
        for initial in self.initialLines:
            text += indent + indentTab
            text += initial.exportIdentifierToLaTeX()
            text += " & "
            text += initial.exportTermToLaTeXTable()
            text += " & "
            text += initial.exportConjunctionToLaTeX(textAnd = textAnd, letters = letters)
            for prime in self.primeImpLines:
                text += " & "
                if set(initial.identifier) <= set(prime.identifier):
                    text += "\\times"
            text += "\\\\\n"
            text += indent + indentTab + "\\hline\n"
        text += indent + "\\end{array}\n"
        return text

    def exportToText(self, letters = None):
        """
        Args:
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')

        Returns:
            str: string representing this covering matrix
        """
        if letters == None:
            letters = list(string.ascii_lowercase)

        columnWidth = []
        for prime in self.primeImpLines:
            width = len(prime.exportIdentifierToText())
            if len(prime.exportTermToText()) > width:
                width = len(prime.exportTermToText())
            if len(prime.exportConjunctionToText()) > width:
                width = len(prime.exportConjunctionToText())
            columnWidth.append(width)

        identifierWidth = 0
        termWidth = 0
        conjunctionWidth = 0
        tableHeaderIndent = ""

        if len(self.initialLines) > 0:
            for initial in self.initialLines:
                if len(initial.exportIdentifierToText()) > identifierWidth:
                    identifierWidth = len(initial.exportIdentifierToText())
                if len(initial.exportTermToText()) > termWidth:
                    termWidth = len(initial.exportTermToText())
                if len(initial.exportConjunctionToText()) > conjunctionWidth:
                    conjunctionWidth = len(initial.exportConjunctionToText())
            tableHeaderIndent += "|        "
            for k in range(identifierWidth):
                tableHeaderIndent += " "
            for k in range(termWidth):
                tableHeaderIndent += " "
            for k in range(conjunctionWidth):
                tableHeaderIndent += " "

        tableHorizontalLine = "-"
        for k in range(len(tableHeaderIndent)):
            tableHorizontalLine += "-"
        for i in range(len(self.primeImpLines)):
            tableHorizontalLine += "---"
            for k in range(columnWidth[i]):
                tableHorizontalLine += "-"

        text = ""
        text += tableHorizontalLine + "\n"

        # first row of the covering matrix (identifiers of the prime implicants)
        text += tableHeaderIndent
        for i in range(len(self.primeImpLines)):
            prime = self.primeImpLines[i]
            text += "| "
            identifier = prime.exportIdentifierToText()
            text += identifier
            for k in range(len(identifier), columnWidth[i]):
                text += " "
            text += " "
        text += "|\n"

        # second row of the covering matrix (representations of the prime implicants)
        text += tableHeaderIndent
        for i in range(len(self.primeImpLines)):
            prime = self.primeImpLines[i]
            text += "| "
            term = prime.exportTermToText()
            text += term
            for k in range(len(term), columnWidth[i]):
                text += " "
            text += " "
        text += "|\n"

        # third row of the covering matrix (prime implicants written as formulas)
        text += tableHeaderIndent
        for i in range(len(self.primeImpLines)):
            prime = self.primeImpLines[i]
            text += "| "
            conjunction = prime.exportConjunctionToText(letters = letters)
            text += conjunction
            for k in range(len(conjunction), columnWidth[i]):
                text += " "
            text += " "
        text += "|\n"

        text += tableHorizontalLine + "\n"

        # the covering matrix
        for initial in self.initialLines:
            text += "| "
            identifier = initial.exportIdentifierToText()
            text += identifier
            for k in range(len(identifier), identifierWidth):
                text += " "
            text += " | "
            term = initial.exportTermToText()
            text += term
            for k in range(len(term), termWidth):
                text += " "
            text += " | "
            conjunction = initial.exportConjunctionToText(letters = letters)
            text += conjunction
            for k in range(len(conjunction), conjunctionWidth):
                text += " "
            text += " "
            for i in range(len(self.primeImpLines)):
                prime = self.primeImpLines[i]
                text += "| "
                numSpacesLeft = (columnWidth[i] - 1) // 2
                numSpacesRight = columnWidth[i] // 2
                for k in range(numSpacesLeft):
                    text += " "
                if set(initial.identifier) <= set(prime.identifier):
                    text += "x"
                else:
                    text += " "
                for k in range(numSpacesRight):
                    text += " "
                text += " "
            text += "|\n"

        if len(self.initialLines) > 0:
            text += tableHorizontalLine + "\n"

        return text

