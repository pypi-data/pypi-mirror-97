#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################
#    This file implement the PopClient class.
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

""" This file implement the PopClient class. """

import poplib

__all__ = [ "PopClient" ]

class PopClient:

    """ This class is a pop3 client to receive email. """

    def __init__(
        self, server="", port=None, username=None, password=None, ssl=True, debug=0
    ):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        if ssl and not port:
            self.port = poplib.POP3_SSL_PORT
        elif not ssl and not port:
            self.port = poplib.POP3_PORT
        self.ssl = ssl
        self.debug = debug

    def create_connection(self):

        """ This method start the connection and authentication. """

        if self.ssl:
            self.mailserver = poplib.POP3_SSL(self.server, self.port)
            # self.mailserver.stls()
        else:
            self.mailserver = poplib.POP3(self.server, self.port)

        if self.ssl:
            self.mailserver.set_debuglevel(self.debug)
            self.mailserver.getwelcome()

        self.mailserver.user(self.username)
        self.mailserver.pass_(self.password)

    def get_all_mail(self, reverse=False):

        """ This method is a generator and return all email. """

        self.create_connection()

        response = self.mailserver.list()
        ids = response[1]
        length = len(ids)
        for i, id_ in enumerate(ids):
            if reverse:
                position = length - i
            else:
                position = i + 1
            yield length, i, b"\r\n".join(self.mailserver.retr(position)[1])

        self.mailserver.quit()
