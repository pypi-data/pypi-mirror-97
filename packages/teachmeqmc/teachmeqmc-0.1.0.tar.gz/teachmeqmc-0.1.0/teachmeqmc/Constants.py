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
    Definitions of global constants.
"""

__all__ = ["VERSION", "__version__"]

# version of the package
VERSION = (0, 1, 0) 
#__version__ = ".".join([str(x) for x in VERSION])
__version__ = str(VERSION[0]) + "." + str(VERSION[1]) + "." + str(VERSION[2])
