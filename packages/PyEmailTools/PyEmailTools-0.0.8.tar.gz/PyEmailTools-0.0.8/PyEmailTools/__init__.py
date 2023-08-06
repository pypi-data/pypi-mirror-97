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

__version__ = "0.0.8"

__all__ = [
	"Forger", "Reader", "ImapClient", "SmtpClient", "PopClient", 
	"forger", "analysis"
]

print("""
PyEmailTools  Copyright (C) 2020, 2021  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
""")

from PyEmailTools.Forger import Forger, main as forger
from PyEmailTools.Reader import Reader, main as analysis
from PyEmailTools.ImapClient import ImapClient
from PyEmailTools.SmtpClient import SmtpClient
from PyEmailTools.PopClient import PopClient