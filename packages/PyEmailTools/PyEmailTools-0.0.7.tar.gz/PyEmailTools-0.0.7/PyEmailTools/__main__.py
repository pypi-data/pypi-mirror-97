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

from PyEmailTools.Forger import main as forger
from PyEmailTools.Reader import main as analysis
from sys import argv

if len(argv) > 1:
	script = argv.pop(1).lower()
	if script == "forger":
		forger()
		exit(0)
	elif script == "analysis":
		analysis()
		exit(0)

print("""USAGES: 
	./PyEmailTools.pyz forger
	./PyEmailTools.pyz analysis
	python3 PyEmailTools.pyz forger
	python3 PyEmailTools.pyz analysis

HELP:
	./PyEmailTools.pyz forger -h
	./PyEmailTools.pyz analysis --help
	python3 PyEmailTools.pyz forger --help
	python3 PyEmailTools.pyz analysis -h
""")
exit(1)
