
teachmeqmc
==========

This package contains an implementation of the Quine-McCluskey algorithm and
serves to educational purposes.

Its main goal is to produce a LaTeX document with detailed description of the
performing of the Quine-McCluskey algorithm for a given input; the input is
represented by a complete Disjunctive Normal Form (shortly DNF) which may
contain duplicate minterms.

The motivation to write this program was to provide university students with
automatically generated examples for better understanding the Quine-McCluskey
algorithm and, furthermore, to randomly generate examen tests on this subject
together with their detailed solutions to make the corrections of the tests
easier.


Installation
------------

Install the package from [PyPI](https://pypi.org/) utilizing the
[pip](https://pypi.org/project/pip/) module:

    python -m pip install teachmeqmc


Example
-------

A simple program using this package may look like this:

```python
    from teachmeqmc import BooleanFunction

    f = BooleanFunction(4)
    f.addTerm((0, 0, 0, 0))
    f.addTerm((0, 0, 0, 1))
    f.addTerm((0, 0, 1, 0))
    f.addTerm((0, 0, 1, 1))
    f.addTerm((0, 1, 0, 0))
    f.addTerm((1, 1, 0, 0))
    f.addTerm((1, 1, 0, 1))
    f.addTerm((1, 0, 0, 1))
    f.addTerm((1, 0, 0, 1))

    f.performQuineMcCluskey()

    f.show()
    f.saveToTextFile("output.txt")
    f.saveToLaTeXFile("output.tex")
```

The program first imports the class `BooleanFunction`.
Then it creates a new instance `f` of the class `BooleanFunction`
which represents a Boolean function (a mapping from {0,1}^n to {0,1}) defined
by its complete DNF.
The parameter `4` gives the number of the inputs of the Boolean function.

Further, by calling the method `addTerm` it is defined by which minterms the
complete DNF of the Boolean function is given; for example 
`f.addTerm((0, 0, 1, 0))` states that the minterm _a'b'cd'_ shall be a part of
the defining complete DNF.
Observe that the last two minterms are identical.
However, both will be part of the defining complete DNF and in the output
report it will be visualised that one of these terms has to be removed.

Then the Quine-McCluskey algorithm is performed; this method does not
return anything, instead, it stores the result of the procedure to the
attributes of `BooleanFunction`.

Finally, calling `show` prints the report on the processing of the Quine-McCluskey
algorithm to the terminal output, calling `saveToTextFile` saves it to a plain text file,
and calling `saveToLaTeXFile` saves it to a LaTeX file which can be further
compiled to a PDF file e.g. by **pdflatex**.

Remark that also single parts of the report may be obtained.
For such an output, see the methods of the class `BooleanFunction` in the form
`export...ToLaTeX` and `export...ToText`.
