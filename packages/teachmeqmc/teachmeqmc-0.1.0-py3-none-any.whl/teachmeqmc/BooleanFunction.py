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
Definition of class `BooleanFunction` which represents a Boolean function given
    by its complete DNF (complete Disjunctive Normal Form) and implements the
    Quine-McCluskey algorithm which finds the minimal DNF of this Boolean function.
"""

__all__ = ["BooleanFunction"]

import copy
import string
import random

from teachmeqmc.CoveringMatrix import *
from teachmeqmc.LineInQuineMcCluskey import *
from teachmeqmc.Utils import *
from teachmeqmc.Constants import *

class BooleanFunction:
    """
    Represents a Boolean function given by its complete DNF (complete
    Disjunctive Normal Form) and implements the Quine-McCluskey algorithm which
    finds the minimal DNF of this Boolean function.

    Recall that Disjunctive Normal Form (DNF) is defined as a disjunction of
    minterms where a minterm is a conjunction of literals where a literal is a
    Boolean variable or a negation of a Boolean variable.

    A Complete Disjunctive Normal Form (CDNF) is a DNF such that every its
    minterm contains all the variables.

    Example:

        Let f:{0,1}^3 -> {0,1} be a Boolean function defined by:

            f(0, 0, 0) = 0
            f(0, 0, 1) = 1
            f(0, 1, 0) = 1
            f(0, 1, 1) = 1
            f(1, 0, 0) = 0
            f(1, 0, 1) = 0
            f(1, 1, 0) = 1
            f(1, 1, 1) = 0

    A CDNF of this function is
        f(a, b, c) = a'b'c + a'bc' + a'bc + abc'

    Here, multiplication stands for the conjunction, addition for the
    disjunction, and ' stands for the negation.

    There are many other DNFs of this function, for example
        f(a, b, c) = a'c + bc'
    is the minimal DNF.

    This class serves to represent such a function and to find its minimal DNF.

    This particular Boolean function can be defined by the Python code:

        f = BooleanFunction(3)
        f.addTerm((0, 0, 1))
        f.addTerm((0, 1, 0))
        f.addTerm((0, 1, 1))
        f.addTerm((1, 1, 0))

    The first line of the code creates a Boolean function f with three inputs.
    The following four lines define those values of the input for which the
    output of the function is 1.
    (For the rest of the outputs it is 0.)
    The minimized DNF is then found by calling:

        f.performQuineMcCluskey()

    This method stores the minimized DNFs together with a report of
    the processing the algorithm to the attributes of this class.
    The report can be obtained by calling:

        f.exportToText()

    for an output in plain text format or by calling:

        f.exportToLaTeX()

    for an output in LaTeX code.

    Attributes:
        numInputs (int): the number of the inputs (arguments) of the Boolean
            function (also: the number of the variables in the CDNF that
            defines this Boolean function)
        steps (list of lists of teachmeqmc.LineInQuineMcCluskey): list of the
            steps that describe the first phase of the Quine-McCluskey algorithm
            (that is, the finding of the prime implicants);

             * each step is a list of lines;
             * each line represents a (possibly merged) term
        lastStep (int): index to `steps` pointing to the last step of the
            algorithm
        termCounter (int): counts terms that have been added by `addTerm`;
            it is utilized to create the identifiers of the terms;
            see attribute `identifier` in `teachmeqmc.LineInQuineMcCluskey`
        coveringMatrices (list of teachmeqmc.CoveringMatrix): step-by-step
            simplifications of the covering matrices
        essentialPrimeImplicants (list of teachmeqmc.LineInQuineMcCluskey): list 
            of those terms that are definitely part of the resulting minimal
            DNF;
            this list is gradually updated by each new member of
            `coveringMatrices`
        result (list of lists of teachmeqmc.LineInQuineMcCluskey): list of minimal DNFs
        comment (str): a comment to this particular instance of `BooleanFunction`;
            It has no impact on the algorithm itself.
            It is just an information that can be used, e.g., to add a title to
            the resulting LaTeX code.
            It has no usage by default.
    """

    def __init__(self, numInputs):
        self.numInputs = numInputs
        self.steps = []
        self.steps.append([])
        self.lastStep = None
        self.termCounter = 0
        self.coveringMatrices = []
        self.essentialPrimeImplicants = []
        self.result = []
        self.comment = ""
        self.permutation = None

    def getCopy(self):
        """Returns a deep copy of this instance of `BooleanFunction`."""
        return copy.deepcopy(self)

    def addTerm(self, inputTuple):
        """
        Defines a value of the input of this Boolean function for which the
        output is 1.

        See the example in the description of this class.

        Args:
            inputTuple (tuple of int): a tuple containg `0` and `1` of the same length as
            is the value of `numInputs`

        Returns nothing, only affects this instance.
        """
        if len(inputTuple) != self.numInputs:
            raise Exception("Size of the parameter inputTuple does not accord with the number of inputs of this Boolean function.")
        else:
            for i in range(self.numInputs):
                if not inputTuple[i] in [0,1]:
                    raise Exception("Invalid value of the given input: " + str(inputTuple[i]))
            self.termCounter += 1
            numTerms = len(self.steps[0])
            #self.steps[0].append(LineInQuineMcCluskey([self.termCounter], inputTuple))
            self.steps[0].append(LineInQuineMcCluskey([numTerms + 1], inputTuple))

    def getValue(self, inputTuple):
        """
        Args:
            inputTuple (tuple of int): a tuple containg `0` and `1` of the same length as
            is the value of `numInputs`; represents the input of the Boolean function

        Returns:
            int: the output value of this Boolean function for the given input
        """
        for line in self.steps[0]:
            if line.term == inputTuple:
                return 1
        return 0

    def permuteTerms(self, perm):
        """
        Permutes the order of the literals in the terms in the definition of
            the Boolean function.

        This is useful to obtain differently looking (yet, actually, the same)
            exercises on Quine-McCluskey algorithm.

        Args:
            perm (tuple of int): the permutation according to which the literals
                are shuffled;
                it is a tuple that contains a permutation of the non-negative
                integers `0, 1, 2, ..., n-1` where `n` is the number of the
                inputs of the Boolean function (see attribute `numInputs`)

        Example:

            The Boolean function given by the example in the description of
            this class is represented by CDNF:

            a'b'c + a'bc' + a'bc + abc'

            By applying `permuteTerms` with `perm` equal to `[1,2,0]`:

             * `a` is rewritten to `b`,
             * `b` is rewritten to `c`,
             * `c` is rewritten to `a`.

            Hence the result will be:

            b'c'a + b'ca' + b'ca + bca'

        Example:

            The following code creates four differently looking exercises with
            exactly the same difficulty.
            Furthermore, the Boolean function of each exercise will be given by
            exactly 8 minterms of the complete DNF (hence duplicate minterms
            will be present).

                from teachmeqmc import BooleanFunction

                f = BooleanFunction(3)
                f.addTerm((0, 0, 0))
                f.addTerm((0, 0, 1))
                f.addTerm((0, 1, 1))
                f.addTerm((1, 1, 0))
                f.addTerm((1, 1, 1))

                permutations = []
                permutations.append((0, 1, 2))
                permutations.append((1, 2, 0))
                permutations.append((2, 0, 1))
                permutations.append((0, 2, 1))

                exercises = []
                for perm in permutations:
                    exercise = f.getCopy()
                    exercise.permuteTerms(perm)
                    exercise.duplicateTerms(8)
                    exercise.shuffleTerms()
                    exercises.append(exercise)

                for i in range(len(exercises)):
                    exercise = exercises[i]
                    exercise.performQuineMcCluskey()
                    exercise.saveToLaTeXFile("exercise_" + str(i) + ".tex")

        Returns nothing, only affects this instance.
        """
        for line in self.steps[0]:
            newTerm = self.numInputs * [None]
            for i in range(self.numInputs):
                newTerm[perm[i]] = line.term[i]
            line.term = tuple(newTerm)

    def negateTerms(self, mask):
        """
        Negates specified literals in the complete DNF that represents the
        processed Boolean function.

        This is useful to obtain differently looking (yet, actually, the same)
        exercises on Quine-McCluskey algorithm.

        Args:
            mask (tuple of int): specifies which literals shall be negated;
                It is a tuple containg `0` and `1` of the same length as is the
                value of `numInputs`.

                 * `0` specifies that the literal shall not be negated,
                 * `1` specifies that the literal shall be negated.

        Example:

            The Boolean function given by the example in the description of
            this class is represented by CDNF:

            a'b'c + a'bc' + a'bc + abc'

            By applying `negateTerms` with `mask` equal to `[1,0,1]`:

             * `a` and `c` are negated,
             * `b` is not negated.

            Hence the result will be:

            ab'c' + abc + abc' + a'bc

        Example:

            The following code creates four differently looking exercises with
            exactly the same difficulty.
            Furthermore, the Boolean function of each exercise will be given by
            exactly 8 minterms of the complete DNF (hence duplicate minterms
            will be present).

                from teachmeqmc import BooleanFunction

                f = BooleanFunction(3)
                f.addTerm((0, 0, 0))
                f.addTerm((0, 0, 1))
                f.addTerm((0, 1, 1))
                f.addTerm((1, 1, 0))
                f.addTerm((1, 1, 1))

                masks = []
                masks.append((0, 0, 0))
                masks.append((0, 0, 1))
                masks.append((0, 1, 0))
                masks.append((0, 1, 1))

                exercises = []
                for mask in masks:
                    exercise = f.getCopy()
                    exercise.negateTerms(mask)
                    exercise.duplicateTerms(8)
                    exercise.shuffleTerms()
                    exercises.append(exercise)

                for i in range(len(exercises)):
                    exercise = exercises[i]
                    exercise.performQuineMcCluskey()
                    exercise.saveToLaTeXFile("exercise_" + str(i) + ".tex")

        Returns nothing, only affects this instance.
        """
        for line in self.steps[0]:
            newTerm = self.numInputs * [None]
            for i in range(self.numInputs):
                if mask[i] == 1:
                    newTerm[i] = 1 - line.term[i]
                else:
                    newTerm[i] = line.term[i]
                #print(i, line.term[i], '->', newTerm[i])
            line.term = tuple(newTerm)

    def duplicateTerms(self, desiredNumberOfTerms):
        """
        Randomly creates redundant (duplicate) terms in the definition of
            this Boolean function.

        Useful when randomly generating examen tests.

        This method will create redundant terms such that the final number of
        the terms that form the complete DNF of this Boolean function is equal
        to or greater than `desiredNumberOfTerms`.

        Args:
            desiredNumberOfTerms (int): by how many terms (in the complete DNF)
                    this Boolean function shall be given

        Returns nothing, only affects this instance.
        """
        numTerms = len(self.steps[0])
        if desiredNumberOfTerms > numTerms:
            for i in range(numTerms, desiredNumberOfTerms):
                j = random.randint(0, numTerms - 1)
                inputTuple = self.steps[0][j].term
                self.addTerm(inputTuple)

    def shuffleTerms(self):
        """
        Randomly shuffles the order of the terms that form the complete DNF of
        this Boolean function.

        Useful when randomly generating examen tests.

        Returns nothing, only affects this instance.
        """
        random.shuffle(self.steps[0])
        for i in range(len(self.steps[0])):
            self.steps[0][i].identifier = [i + 1]

    def setComment(self, comment):
        """
        Sets the value of the attribute `comment` which serves as an optional
        description of this instance.
        """
        self.comment = comment

    def getComment(self):
        """
        Returns the value of the attribute `comment` which serves as an
        optional description of this instance.
        """
        return self.comment

    def createNextStep(self, stepIndex):
        """
        Creates the subsequent step by merging terms of the current step.

        A step is represented by a list of terms (instances of
        `teachmeqmc.LineInQuineMcCluskey`) and it is an item in the list
        `steps`.

        Args:
            stepIndex (int): the current step (index in the list `steps`)

        Returns:
            reference to list of teachmeqmc.LineInQuineMcCluskey: reference to
                the new step (reference to list of instances of
                `LineInQuineMcCluskey`; hence not an index in a list)
        """
        currentStep = self.steps[stepIndex]
        newStep = []
        l = len(currentStep)
        for i in range(l):
            line1 = currentStep[i]
            if not line1.removed:
                for j in range(i, l, 1):
                    line2 = currentStep[j]
                    if not line2.removed:
                        newLine = line1.mergeWith(line2)
                        if newLine != None:
                            newStep.append(newLine)
        return newStep

    def removeDuplicates(self, stepIndex):
        """
        Marks redundant (duplicate) terms in the current step as 'removed'.

        The terms are represented by instances of
            `teachmeqmc.LineInQuineMcCluskey`.

        The duplicate terms (lines) are not actually deleted, only their
            attribute `removed` is set to `True`.

        Args:
            stepIndex (int): the current step (index in the list `steps`)

        Returns nothing, only affects this instance.
        """
        step = self.steps[stepIndex]
        l = len(step)
        for i in range(l):
            line1 = step[i]
            for j in range(i+1, l, 1):
                line2 = step[j]
                if line1.term == line2.term:
                    line2.removed = True

    def performQuineMcCluskey(self):
        """
        Performs the Quine-McCluskey algorithm in order to find the minimal
            DNFs.

        As the input of this procedure, the list of terms given by
            `self.steps[0]` is taken.

        The output of this method is stored to the attributes:

         * `steps` ... list of terms where each subsequent one is given by
                merging the terms of the preceding one
         * `coveringMatrices` ... list of covering matrices representing their
                gradual simplifications

        These two attributes are needed when calling the methods
            `BooleanFunction.exportCoveringMatricesToLaTeX` and
            `BooleanFunction.exportStepsToTex` to obtain the
            description of the run of the algorithm in LaTeX format.

        Returns nothing, only affects this instance.
        """
        # Find prime implicants by merging terms
        stepIndex = 0
        self.removeDuplicates(0)
        while stepIndex < self.numInputs:
            newStep = self.createNextStep(stepIndex)
            if newStep != []:
                self.steps.append(newStep)
                stepIndex += 1
                self.removeDuplicates(stepIndex)
            else:
                break
        self.lastStep = stepIndex
        # Covering matrix
        self.primeImpLines = []
        for step in self.steps:
            for line in step:
                if not line.used and not line.removed:
                    self.primeImpLines.append(line)
        self.coveringMatrices = []
        # First covering matrix which contains all the initial terms and prime implicants
        covMat = CoveringMatrix(initialLines = self.steps[0], primeImpLines = self.primeImpLines, numInputs = self.numInputs)
        covMat.removeRedundantInitialLines()
        self.coveringMatrices.append(covMat)
        self.essentialPrimeImplicants = []
        # Gradual simplifications of the covering matrix.
        # The terms that are, during the procedure, recognized as being
        # definitely part of the resulting minimal DNF, are stored to
        # `essentialPrimeImplicants`.
        done = False
        while not done:
            done = True
            if not self.coveringMatrices[-1].isEmpty():
                covMat = CoveringMatrix(parentCoveringMatrix = self.coveringMatrices[-1], numInputs = self.numInputs, comment = "essential")
                primeImplicants = covMat.findAndRemoveEssentialPrimeImplicants()
                if primeImplicants != []:
                    primeImplicants.reverse()
                    self.essentialPrimeImplicants.extend(primeImplicants)
                    self.coveringMatrices.append(covMat)
                    done = False
            if not self.coveringMatrices[-1].isEmpty():
                covMat = CoveringMatrix(parentCoveringMatrix = self.coveringMatrices[-1], numInputs = self.numInputs, comment = "prime")
                anythingRemoved = covMat.findAndRemovePrimeImpLinesThatAreSubsets()
                if anythingRemoved:
                    self.coveringMatrices.append(covMat)
                    done = False
            if not self.coveringMatrices[-1].isEmpty():
                covMat = CoveringMatrix(parentCoveringMatrix = self.coveringMatrices[-1], numInputs = self.numInputs, comment = "initial")
                anythingRemoved = covMat.findAndRemoveInitialLinesThatAreSupersets()
                if anythingRemoved:
                    self.coveringMatrices.append(covMat)
                    done = False
        if self.coveringMatrices[-1].isEmpty():
            self.result = []
            self.result.append(self.essentialPrimeImplicants)
        else:
            # If the covering matrix is not emty at this moment, we are going to
            #   use a brute force method.
            # Brute force method = examine all the possible subsets (hence
            #   exponential complexity)
            self.result = []
            bruteForceResults = self.coveringMatrices[-1].getResultsByBruteForce()
            for brute in bruteForceResults:
                dnf = copy.deepcopy(self.essentialPrimeImplicants)
                dnf.extend(brute)
                self.result.append(dnf)

    def exportCoveringMatricesToLaTeX(self,
            textAnd = "\\land",
            letters = None,
            indent = "",
            indentTab = "    "):
        """
        Args:
            textAnd (str, optional): LaTeX macro for conjunction
                (by default: `\\land`)
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')
            indent (str, optional): text written at the beginning of each line to perform
                indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform indenting of
                more nested parts of the resulting LaTeX code
                (by default: string with four spaces)

        Returns:
            str: LaTeX code describing the covering matrices using the LaTeX
                environment `{array}`.
        """
        if letters == None:
            letters = list(string.ascii_lowercase)
        text = ""
        for covMat in self.coveringMatrices:
            textTable = covMat.exportToLaTeX(
                    textAnd = textAnd,
                    letters = letters,
                    indent = indent + indentTab,
                    indentTab = indentTab)
            if textTable != "":
                if covMat.comment == "essential":
                    text += indent + "Removed essential prime implicants:\n"
                elif covMat.comment == "prime":
                    text += indent + "Removed those columns that are a subset of another column (prime dominance):\n"
                elif covMat.comment == "initial":
                    text += indent + "Removed those rows that are a superset of another row (minterm dominance):\n"
                if not covMat.isEmpty():
                    text += indent + r'\begin{displaymath}' + "\n"
                    text += textTable
                    text += indent + r'\end{displaymath}' + "\n"
        if self.coveringMatrices[-1].isEmpty():
            #text += indent + "\\begin{itemize}\n"
            #text += indent + indentTab + "\\item[\\dots] The cyclic core is empty.\n"
            #text += indent + "\\end{itemize}\n"
            text += indent + "The cyclic core is empty.\n"
        else:
            #text += indent + "\\begin{itemize}\n"
            #text += indent + indentTab + "\\item[\\dots] The cyclic core is not empty.\n"
            #text += indent + "\\end{itemize}\n"
            text += indent + "The cyclic core is not empty.\n"
        return text

    def exportCoveringMatricesToText(self, letters = None):
        """
        Args:
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')

        Returns:
            str: string describing the covering matrices; suitable to be
                printed on the terminal output
        """
        if letters == None:
            letters = list(string.ascii_lowercase)
        text = ""
        for covMat in self.coveringMatrices:
            textTable = covMat.exportToText(letters = letters)
            if textTable != "":
                if covMat.comment == "essential":
                    text += "Removed essential prime implicants:\n"
                elif covMat.comment == "prime":
                    text += "Removed those columns that are a subset of another column (prime dominance):\n"
                elif covMat.comment == "initial":
                    text += "Removed those rows that are a superset of another row (minterm dominance):\n"
                text += textTable
        if self.coveringMatrices[-1].isEmpty():
            text += "The cyclic core is empty.\n"
        else:
            text += "The cyclic core is not empty.\n"
        return text

    def exportCDNFToLaTeXAsAlign(self,
            name = "\\varphi",
            lineLength = 65,
            textOr = "\\lor",
            textAnd = "\\land",
            parentheses = True,
            letters = None,
            indent = "",
            indentTab = "    "):
        """
        Args:
            name (str, optional): name of the formula in LaTeX code
                (by default: `\\varphi`)
            lineLength (int, optional): maximal number of LaTeX symbols that
                can appear on one line of the output (the line will be broken
                before its length exceeds `lineLength`)
            textOr (str, optional): LaTeX macro for disjunction
                (by default: `\\lor`)
            textAnd (str, optional): LaTeX macro for conjunction
                (by default: `\\land`)
            parentheses (bool, optional): indicates whether the terms shall be enclosed
                in (round) parentheses
                (by default: `True`)
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')
            indent (str, optional): text written at the beginning of each line
                to perform indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform
                indenting of more nested parts of the resulting LaTeX code
                (by default: string with four spaces)

        Returns:
            str: LaTeX code describing the initial terms (the definition of
                this Boolean function) as a complete DNF using the LaTeX
                environment `{align}`.
        """
        if letters == None:
            letters = list(string.ascii_lowercase)
        text = ""
        text += indent + "\\begin{align*}\n"
        text += indent + name + " \\equiv & \n"
        if textAnd != "":
            withConjunctions = True
        else:
            withConjunctions = False
        withNegations = True
        lineCounter = 0
        text += indent
        if len(self.steps) > 0:
            first = True
            for term in self.steps[0]:
                termLength = term.getConjunctionLength(withConjunctions = withConjunctions, withNegations = withNegations)
                if not first and textOr != "":
                    termLength += 1
                if parentheses:
                    termLength += 2

                if lineCounter + termLength > lineLength:
                    text += "\\\\\n"
                    text += indent + indentTab + "& \n"
                    text += indent + indentTab
                    lineCounter = 0
                else:
                    lineCounter += termLength

                if not first:
                    text += "{" + textOr + "}"
                if parentheses:
                    text += "\\left("
                text += term.exportConjunctionToLaTeX(textAnd = textAnd, letters = letters)
                if parentheses:
                    text += "\\right)"

                if first:
                    first = False
        else:
            text += "0"
        text += "\n"
        text += indent + "\\end{align*}\n"
        return text

    def exportCDNFToLaTeX(self,
        name = "\\varphi",
        textOr = "\\lor",
        textAnd = "\\land",
        parentheses = True,
        letters = None):
        """
        Args:
            name (str, optional): name of the formula in LaTeX code
                (by default: `\\varphi`)
            textOr (str, optional): LaTeX macro for disjunction
                (by default: `\\lor`)
            textAnd (str, optional): LaTeX macro for conjunction
                (by default: `\\land`)
            parentheses (bool, optional): indicates whether the terms shall be enclosed
                in (round) parentheses
                (by default: `True`)
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')

        Returns:
            str: LaTeX code describing the initial terms (the definition of
                this Boolean function) as a complete DNF

        The DNF is written in-line, compare with
            `BooleanFunction.exportCDNFToLaTeXAsAlign`.
        """
        if letters == None:
            letters = list(string.ascii_lowercase)
        text = ""
        text += "$" + name + "{\\equiv}$ "
        first = True
        counter = 0
        for term in self.steps[0]:
            if first:
                first = False
            else:
                text += " ${" + textOr + "}$ "
            text += " $"
            if parentheses:
                text += "\\left("
            text += term.exportConjunctionToLaTeX(textAnd = textAnd, letters = letters)
            if parentheses:
                text += "\\right)"
            text += "$ "
            counter += 1
        if counter == 0:
            text += " $0$ "
        return text

    def exportCDNFToText(self, letters = None, indent = ""):
        """
        Args:
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')
            indent (str, optional): text written at the beginning of each line to perform
                indenting
                (by default: empty string)

        Returns:
            str: string describing the initial terms (the definition of this
                Boolean function) as a complete DNF
        """
        if letters == None:
            letters = list(string.ascii_lowercase)
        text = ""
        outLine = indent
        outLine += "f("
        for i in range(self.numInputs):
            if i > 0:
                outLine += ","
            outLine += letters[i]
        outLine += ") = "
        for i in range(len(self.steps[0])):
            term = self.steps[0][i]
            if len(outLine) + 3 + len(term.exportConjunctionToText(letters = letters)) >= 76:
                text += outLine + "\n"
                outLine = indent
            if i > 0:
                outLine += "+ "
            outLine += term.exportConjunctionToText(letters = letters) + " "
        text += outLine + "\n"
        return text

    def exportResultToLaTeXAsAlign(self,
        name = "\\varphi",
        lineLength = 65,
        textOr = "\\lor",
        textAnd = "\\land",
        parentheses = True,
        letters = None,
        indent = "",
        indentTab = "    "):
        """
        Args:
            name (str, optional): name of the formula in LaTeX code
                (by default: `\\varphi`)
            lineLength (int, optional): maximal number of LaTeX symbols that
                can appear on one line of the output (the line will be broken
                before its length exceeds `lineLength`)
            textOr (str, optional): LaTeX macro for disjunction
                (by default: `\\lor`)
            textAnd (str, optional): LaTeX macro for conjunction
                (by default: `\\land`)
            parentheses (bool, optional): indicates whether the terms shall be enclosed
                in (round) parentheses
                (by default: `True`)
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')
            indent (str, optional): text written at the beginning of each line
                to perform indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform
                indenting of more nested parts of the resulting LaTeX code
                (by default: string with four spaces)

        Returns:
            str: LaTeX code describing the resulting minimized DNFs using the
                LaTeX environment `{align}`.
        """
        if letters == None:
            letters = list(string.ascii_lowercase)
        if textAnd != "":
            withConjunctions = True
        else:
            withConjunctions = False
        withNegations = True
        text = ""
        if self.result != []:
            text += indent + "\\begin{align*}\n"
            firstDNF = True
            dnfCounter = 0
            for dnf in self.result:
                if firstDNF:
                    firstDNF = False
                else:
                    text += "\\\\\n"
                dnfCounter += 1
                text += indent + indentTab + name
                if len(self.result) > 1:
                    text += "_{" + str(dnfCounter) + "}"
                text += " \\equiv & "
                lineCounter = 0
                if len(dnf) > 0:
                    firstTerm = True
                    for term in dnf:
                        termLength = term.getConjunctionLength(withConjunctions = withConjunctions, withNegations = withNegations)
                        if not firstTerm and textOr != "":
                            termLength += 1
                        if parentheses:
                            termLength += 2

                        if lineCounter + termLength > lineLength:
                            text += "\\\\\n"
                            text += indent + indentTab + "& \n"
                            text += indent + indentTab
                            lineCounter = 0
                        else:
                            lineCounter += termLength

                        if not firstTerm:
                            text += "{" + textOr + "}"
                        if parentheses:
                            text += "\\left("
                        text += term.exportConjunctionToLaTeX(textAnd = textAnd, letters = letters)
                        if parentheses:
                            text += "\\right)"

                        if firstTerm:
                            firstTerm = False
                else:
                    text += "0"
            text += "\n"
            text += indent + "\\end{align*}\n"
        return text

    def exportResultToText(self, letters = None, indent = ""):
        """
        Args:
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')
            indent (str, optional): text written at the beginning of each line to perform
                indenting
                (by default: empty string)

        Returns:
            str: string describing the resulting minimized DNFs; suitable to
                write a report to a terminal output

        """
        if letters == None:
            letters = list(string.ascii_lowercase)
        text = ""
        outLine = indent
        if self.result != []:
            for i in range(len(self.result)):

                dnf = self.result[i]

                if i > 0:
                    text += outLine + "\n"
                    outLine = indent

                outLine += "f"
                if len(self.result) > 1:
                    outLine += str(i + 1)
                outLine += "("
                for i in range(self.numInputs):
                    if i > 0:
                        outLine += ","
                    outLine += letters[i]
                outLine += ") = "

                for j in range(len(dnf)):
                    term = dnf[j]
                    if len(outLine) + 3 + len(term.exportConjunctionToText(letters = letters)) >= 76:
                        text += outLine + "\n"
                        outLine = indent
                    if j > 0:
                        outLine += "+ "
                    outLine += term.exportConjunctionToText(letters = letters) + " "
                text += outLine + "\n"
                outLine = indent
        return text

    def exportResultToLaTeX(self,
        name = "\\varphi",
        textOr = "\\lor",
        textAnd = "\\land",
        parentheses = True,
        letters = None):
        """
        Args:
            name (str, optional): name of the formula in LaTeX code
                (by default: `\\varphi`)
            textOr (str, optional): LaTeX macro for disjunction
                (by default: `\\lor`)
            textAnd (str, optional): LaTeX macro for conjunction
                (by default: `\\land`)
            parentheses (bool, optional): indicates whether the terms shall be enclosed
                in (round) parentheses
                (by default: `True`)
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')

        Returns:
            str: LaTeX code describing the resulting minimized DNF

        The DNF is written in-line, compare with
            `BooleanFunction.exportResultToLaTeXAsAlign`.
        """
        if letters == None:
            letters = list(string.ascii_lowercase)
        text = ""
        if self.result != []:
            for i in range(len(self.result)):
                if i > 0:
                    text += ", "
                dnf = self.result[i]
                text += "$" + name
                if len(self.result) > 1:
                    text += "_{" + str(i + 1) + "}"
                text += "{\\equiv}"
                dnfLen = len(dnf)
                if dnfLen == 0:
                    text += "0"
                else:
                    for j in range(dnfLen):
                        term = dnf[j]
                        if j > 0:
                            text += "{" + textOr + "}"
                        if parentheses:
                            text += "\\left("
                        text += term.exportConjunctionToLaTeX(textAnd = textAnd, letters = letters)
                        if parentheses:
                            text += "\\right)"
                text += "$"
        return text

    def exportAsKarnaughMapToTikZ(self,
        tikzOptions = "",
        letters = None,
        indent = "",
        indentTab = "    "):
        """
        Args:
            tikzOptions (str): additional TikZ options for this image
                (by default: empty string)
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')
            indent (str, optional): text written at the beginning of each line to perform
                indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform indenting of
                more nested parts of the resulting LaTeX code
                (by default: string with four spaces)

        Returns:
            str: TikZ code describing the initial terms (the definition of this
                Boolean function) as a Karnaugh map
        """
        if letters == None:
            letters = list(string.ascii_lowercase)
        numInputsOnLeft = self.numInputs // 2
        numInputsOnTop = (self.numInputs + 1) // 2
        numRows = 2 ** numInputsOnLeft
        numCols = 2 ** numInputsOnTop
        leftGrayCode = generateGrayCode(numInputsOnLeft)
        topGrayCode = generateGrayCode(numInputsOnTop)

        text = r''
        text += indent + r'% Karnaugh map representing the Boolean function which is the input of the Quine-McCluskey algorithm' + "\n"
        text += indent + r'\begin{tikzpicture}'
        if tikzOptions != "":
            text += r'[' + tikzOptions + r']'
        text += "\n"

        text += indent + indentTab + r'% inner horizontal lines of the map' + "\n"
        if numRows <= 2:
            for j in range(numRows - 1):
                text += indent + indentTab
                text += r'\draw (-0.5, ' + str(-j - 0.5) + ') -- (' + str(numCols - 0.5) + ', ' + str(-j - 0.5) + ');'
                text += "\n"
        else:
            text += indent + indentTab + r'\foreach \y in {0, 1, ..., ' + str(numRows - 2) + '}{' + "\n"
            text += indent + 2*indentTab
            text += r'\draw (-0.5, -\y - 0.5) -- (' + str(numCols - 0.5) + r', -\y - 0.5);' + "\n"
            text += indent + indentTab + r'}' + "\n"

        text += indent + indentTab + r'% inner vertical lines of the map' + "\n"
        if numCols <= 2:
            for i in range(numCols - 1):
                text += indent + indentTab
                text += r'\draw (' + str(i + 0.5) + ', 0.5) -- (' + str(i + 0.5) + ', ' + str(-numRows + 0.5) + ');'
                text += "\n"
        else:
            text += indent + indentTab + r'\foreach \x in {0, 1, ..., ' + str(numCols - 2) + '}{' + "\n"
            text += indent + 2*indentTab
            text += r'\draw (\x + 0.5, 0.5) -- (\x + 0.5, ' + str(-numRows + 0.5) + ');' + "\n"
            text += indent + indentTab + r'}' + "\n"

        text += indent + indentTab + r'% thick border around the map' + "\n"
        text += indent + indentTab + r'\draw[very thick] (-0.5, 0.5)'
        text += r' -- (' + str(numCols - 0.5) + ', 0.5)'
        text += r' -- (' + str(numCols - 0.5) + ', ' + str(-numRows + 0.5) + ')'
        text += r' -- (-0.5, ' + str(-numRows + 0.5) + ')'
        text += r' -- cycle;' + "\n"

        text += indent + indentTab + r'% names of the variables' + "\n"
        letterIndex = 0
        for k in range(numInputsOnLeft):
            xPos = -1 - 0.5 * (numInputsOnLeft - k - 1)
            text += indent + indentTab
            text += r'\node[below] at (' + str(xPos) + ', ' + str(-numRows + 0.5) + ') '
            text += r'{$' + letters[letterIndex] + '$};' + "\n"
            letterIndex += 1
        for k in range(numInputsOnTop):
            yPos = 1 + 0.5 * (numInputsOnTop - k - 1)
            text += indent + indentTab
            text += r'\node[right] at (' + str(numCols - 0.5) + ', ' + str(yPos) + ') '
            text += r'{$' + letters[letterIndex] + '$};' + "\n"
            letterIndex += 1

        if leftGrayCode != None:
            text += indent + indentTab + r'% bars on left side of the map denoting the input values in Gray code' + "\n"
            for i in range(numRows):
                for k in range(numInputsOnLeft):
                    if leftGrayCode[i][k] == 1:
                        xPos = -1 - 0.5 * (numInputsOnLeft - k - 1)
                        text += indent + indentTab
                        text += r'\draw[ultra thick] (' + str(xPos) + ', ' + str(-i + 0.5) + ')'
                        text += r' -- (' + str(xPos) + ', ' + str(-i - 0.5) + ');' + "\n"
        if topGrayCode != None:
            text += indent + indentTab + r'% bars on top side of the map denoting the input values in Gray code' + "\n"
            for j in range(numCols):
                for k in range(numInputsOnTop):
                    if topGrayCode[j][k] == 1:
                        yPos = 1 + 0.5 * (numInputsOnTop - k - 1)
                        text += indent + indentTab
                        text += r'\draw[ultra thick] (' + str(j - 0.5) + ', ' + str(yPos) + ')'
                        text += r' -- (' + str(j + 0.5) + ', ' + str(yPos) + ');' + "\n"

        text += indent + indentTab + r'% output values inside the map' + "\n"
        for i in range(numRows):
            for j in range(numCols):
                inputTuple = ()
                if leftGrayCode != None:
                    inputTuple += leftGrayCode[i]
                if topGrayCode != None:
                    inputTuple += topGrayCode[j]
                value = self.getValue(inputTuple)
                if value != 0:
                    text += indent + indentTab
                    text += r'\node at (' + str(j) + ', ' + str(-i) + ') '
                    text += r'{$' + str(value) + '$};' + "\n"

        text += indent + r'\end{tikzpicture}' + "\n"
        return text

    def exportStepToLaTeX(self, step, indent = "", indentTab = "    "):
        """
        Args:
            step (list of teachmeqmc.LineInQuineMcCluskey): list of terms 
            indent (str, optional): text written at the beginning of each line
                to perform indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform
                indenting of more nested parts of the resulting LaTeX code (by
                default: string with four spaces)

        Returns:
            str: LaTeX code describing one step of the first phase of the
                Quine-McCluskey algorithm using the LaTeX environment `{array}`
        """
        text = ""
        if len(step) > 0:
            text += indent + "\\begin{array}{r"
            for i in range(self.numInputs):
                text += "c@{\\;}"
            text += "c}\n"

            first = True
            for line in step:
                if first:
                    first = False
                else:
                    text += "\\\\\n"
                text += line.exportToLaTeX(indent = indent + indentTab)
            text += "\n"
            text += indent + "\\end{array}\n"
        return text

    def exportStepsToTex(self, indent = "", indentTab = "    "):
        """
        Args:
            indent (str, optional): text written at the beginning of each line
                to perform indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform
                indenting of more nested parts of the resulting LaTeX code (by
                default: string with four spaces)

        Returns:
            str: LaTeX code describing all the steps of the first phase of the
                Quine-McCluskey algorithm

        See:
            `BooleanFunction.exportStepToLaTeX`
        """
        text = ""
        counter = 0
        for step in self.steps:
            stepText = self.exportStepToLaTeX(step, indent = indent, indentTab = indentTab)
            if stepText == "":
                break
            if counter > 0:
                text += indent + "\\to\n"
            text += stepText
            counter += 1
        return text

    def exportToLaTeX(self,
            name = "\\varphi",
            lineLength = 65,
            textOr = "\\lor",
            textAnd = "\\land",
            parentheses = True,
            letters = None,
            indent = "",
            indentTab = "    "):
        """
        KWArgs:
            name (str, optional): name of the formula in LaTeX code
                (by default: `\\varphi`)
            lineLength (int, optional): maximal number of LaTeX symbols that
                can appear on one line of the output (the line will be broken
                before its length exceeds `lineLength`)
            textOr (str, optional): LaTeX macro for disjunction
                (by default: `\\lor`)
            textAnd (str, optional): LaTeX macro for conjunction
                (by default: `\\land`)
            parentheses (bool, optional): indicates whether the terms shall be enclosed
                in (round) parentheses
                (by default: `True`)
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')
            indent (str, optional): text written at the beginning of each line
                to perform indenting
                (by default: empty string)
            indentTab (str, optional): text written after `indent` to perform
                indenting of more nested parts of the resulting LaTeX code
                (by default: string with four spaces)

        Returns:
            str: LaTeX code describing a report on the whole process of the
                Quine-McCluskey algorithm
        """
        text = ""
        text += r'\noindent\textbf{Exercise:}' + "\n"
        text += r'    Find the minimal disjunctive none forms of the Boolean function given by' + "\n"
        text += r'    its complete disjunctive none form:' + "\n"
        text += self.exportCDNFToLaTeXAsAlign(
                name = name,
                lineLength = lineLength,
                textOr = textOr,
                textAnd = textAnd,
                parentheses = parentheses,
                letters = letters,
                indent = indent + indentTab,
                indentTab = indentTab)
        text += "\n"
        text += r'\noindent\textbf{Solution:}' + "\n"
        text += "\n"
        text += r'\noindent Karnaugh map of the function:' + "\n"
        text += "\n"
        text += r'\begin{center}' + "\n"
        text += self.exportAsKarnaughMapToTikZ(
                tikzOptions = "scale=0.7",
                letters = letters,
                indent = indent + indentTab,
                indentTab = indentTab)
        text += r'\end{center}' + "\n"
        text += "\n"
        text += r'\noindent First phase of the Quine-McCluskey algorithm' + "\n"
        text += r'    (merging terms in order to find prime implicants):' + "\n"
        text += r'\begin{displaymath}' + "\n"
        text += self.exportStepsToTex(indent = indent + indentTab, indentTab = indentTab)
        text += r'\end{displaymath}' + "\n"
        text += "\n"
        text += r'\noindent Second phase of the Quine-McCluskey algorithm (simplifications of' + "\n"
        text += r'    the covering matrix):' + "\n"
        text += self.exportCoveringMatricesToLaTeX(
                textAnd = textAnd,
                letters = letters,
                indent = indent,
                indentTab = indentTab)
        text += "\n"
        text += r'\noindent The resulting minimal disjunctive normal form(s):' + "\n"
        text += self.exportResultToLaTeXAsAlign(
                name = name,
                lineLength = lineLength,
                textOr = textOr,
                textAnd = textAnd,
                parentheses = parentheses,
                letters = letters,
                indent = indent + indentTab,
                indentTab = indentTab)
        text += "\n"
        return text

    def saveToLaTeXFile(self, path):
        """
        Saves a report on the whole process of the Quine-McCluskey algorithm
            to a LaTeX file.

        Args:
            path (str): path to the LaTeX file

        Produces a text file with LaTeX code.

        Returns nothing and does not affect this instance.
        """
        with open(path, "w") as out:
            out.write(getLaTeXHead())
            out.write(self.exportToLaTeX())
            out.write(getLaTeXFoot())

    def exportToText(self, letters = None):
        """
        Args:
            letters (list of str, optional): list of symbols which will be used to
                denote the variables in the conjunction
                (by default: lower case letters starting by 'a')

        Returns:
            str: string describing a report on the whole process of the
                Quine-McCluskey algorithm; suitable to be printed on terminal
                output

        """
        text = ""
        text += "============================================================================\n"
        text += "\n"
        text += "  Find the minimal disjunctive none forms of the Boolean function given by\n"
        text += "  its complete disjunctive none form:\n"
        text += "\n"
        text += self.exportCDNFToText(letters = letters, indent = "    ")
        text += "\n"
        text += "============================================================================\n"
        text += "\n"
        text += "============================================================================\n"
        text += "  First phase of the Quine-McCluskey algorithm (finding prime implicants):\n"
        text += "============================================================================\n"
        text += "\n"
        #TODO the step that exceed 76 characters of the terminal width should
        #   be written below the previously written steps
        outLines = []
        outLineWidth = 0
        first = True
        for i in range(len(self.steps)):
            step = self.steps[i]
            lineWidth = 0
            for j in range(len(step)):
                line = step[j]
                if len(line.exportToText()) > lineWidth:
                    lineWidth = len(line.exportToText())
            for j in range(len(step)):
                line = step[j]
                if j >= len(outLines):
                    while j >= len(outLines):
                        outLines.append("")
                    for k in range(outLineWidth):
                        outLines[j] += " "
                if not first:
                    outLines[j] += "    "
                exportedLine = line.exportToText()
                for k in range(len(exportedLine), lineWidth):
                    outLines[j] += " "
                outLines[j] += exportedLine
            if len(outLines) > 0:
                outLineWidth = len(outLines[0])
            first = False
            #text += "----------------------------------------------------------------\n"
        for outLine in outLines:
            text += outLine + "\n"
        text += "\n"
        text += "===========================================================================\n"
        text += "  Second phase of the algorithm (simplifications of the covering matrix):\n"
        text += "===========================================================================\n"
        text += "\n"
        text += self.exportCoveringMatricesToText()
        text += "\n"
        text += "============================================================================\n"
        text += "\n"
        text += "  The resulting minimal disjunctive normal form(s):\n"
        text += "\n"
        text += self.exportResultToText(letters = letters, indent = "    ")
        text += "\n"
        text += "============================================================================\n"
        return text

    def saveToTextFile(self, path):
        """
        Saves a report on the whole process of the Quine-McCluskey algorithm
            to a text file.

        Args:
            path (str): path to the file

        Produces a text file.

        Returns nothing and does not affect this instance.
        """
        with open(path, "w") as out:
            out.write(self.exportToText())

    def show(self):
        """
        Exports a report on the whole process of the Quine-McCluskey algorithm to
            the terminal output.

        Returns nothing and does not affect this instance.
        """
        print(self.exportToText())

