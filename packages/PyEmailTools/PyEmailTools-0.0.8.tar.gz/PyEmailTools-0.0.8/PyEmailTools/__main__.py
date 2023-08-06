#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################
#    This package implement tools for email analysis and email forgering.
#    Copyright (C) 2020, 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
    This package implement tools for email analysis and email forgering.
"""

try:
    from .Forger import main as forger
    from .Reader import main as analysis
except ImportError:
    from Forger import main as forger
    from Reader import main as analysis
from sys import argv
from os import path

if len(argv) > 1:
    script = argv.pop(1).lower()
    if script == "forger":
        forger()
        exit(0)
    elif script == "analysis":
        analysis()
        exit(0)

print(f"""USAGES: 
    {path.basename(argv[0])} forger
    {path.basename(argv[0])} analysis

HELP:
    {path.basename(argv[0])} forger -h
    {path.basename(argv[0])} analysis --help
""")
exit(1)
