#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################
#    This file implement the GPG class.
#    Copyright (C) 2020  Maurice Lambert

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

""" This file implement the GPG class. """

try:
    import gnupg
except ModuleNotFoundError:
    GNUP_IMPORT = False
else:
    GNUP_IMPORT = True


class GPG:
    """ Class to crypt, sign, decrypt and verfiy a signed email. """

    pass
