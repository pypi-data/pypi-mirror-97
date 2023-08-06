#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    MusaMusa-Fal Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-Fal.
#    MusaMusa-Fal is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-Fal is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-Fal.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    MusaMusa-Fal project : musamusa/musamusa_fal/fal.py

    Use this package to store a filename and a line number.

    ___________________________________________________________________________

    o FileAndLine class
"""
from dataclasses import dataclass


@dataclass
class FileAndLine():
    """
        FileAndLine class

        Use this store to store a filename and a line number into this file.


        !!! Beware, lineindex is greater or equal to 1 !!!
    """
    #         o filename : (str) path to the read source file
    #         o lineindex      : (int) the read line (>=1, first read line is line number 1 !)
    filename: str = ""
    lineindex: str = ""

    def __repr__(self):
        """
            FileAndLine.__repr__()
        """
        res = "{filename}#{lineindex}"
        return res.format(filename=self.filename,
                          lineindex=self.lineindex)
