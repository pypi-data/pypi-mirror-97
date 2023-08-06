#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################
#    This file implement Email class and Constante class.
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

""" This file implement Email class and Constante class. """

from enum import Enum
import email.message
import re

__all__ = [ "Email", "Constantes" ]


class Constantes(Enum):

    REGEX_EMAIL = "([a-zA-Z0-9 ]* ?[<][\w\.+-]+@([\w-]+\.)+[\w-]{2,4}[>])|([\w\.+-]+@([\w-]+\.)+[\w-]{2,4})"


class Email:

    """ This class define email attributs and email methods. """

    def __init__(self):
        self.ips = []
        self.address = []
        self.headers = {}
        self.part = {}
        self.attachements = {}
        self.binary = {}

    def check_email(self, email: str) -> bool:

        """ This method check an email address. """

        email = re.match(Constantes.REGEX_EMAIL.value, email)
        if email:
            return email.group()
        else:
            return False

    def print(
        self,
        ips: bool = True,
        address: bool = True,
        headers: bool = True,
        part: bool = False,
        attachements: bool = False,
        email: email.message.Message = None,
    ) -> None:

        """This method print a email and extract important informations.
        Use it for email analysis."""

        if ips:
            print("IP :")
            for ip in self.ips:
                print(f"\t{ip}")
        if address:
            print("address :")
            for address in self.address:
                print(f"\t{address}")
        if headers:
            print("Headers")
            print(self.headers_to_string())

        if part:
            print("Part : ")
            print(self.part_to_string(self.part))
        if attachements:
            print("Attachement : ")
            print(self.part_to_string(self.attachements))
        if email:
            print("Email : ")
            print(str(email))

    def headers_to_string(self) -> str:

        """ This method return a printable string of email headers. """

        string = ""
        for key, value in self.headers.items():
            value = "\n".join(value)
            if "\n" in value:
                value = value.replace("\n", "\n\t\t")
                string += f"\t{key}\n\t\t{value}\n"
            else:
                string += f"\t{key}\t{value}\n"
        return string

    def part_to_string(self, part) -> str:

        """ This method return string of email part. """

        string = ""
        for key, value in part.items():
            if isinstance(value, str):
                value = value.replace("\n", "\n\t\t")
            else:
                value = str(value).replace("\n", "\n\t\t")
            string += f"\t{key}\n\t\t{value}\n"
        return string

    def save_in_file(self, filename):

        """ This method save your email in file. """

        file = open(filename, "w")
        file.write(self.email.as_string())
        file.close()
        print(f"Your email is saved in {filename}")
