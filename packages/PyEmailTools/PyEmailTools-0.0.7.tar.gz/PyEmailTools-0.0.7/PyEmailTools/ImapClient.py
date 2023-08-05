#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################
#    This file implement the ImapClient class.
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

""" This file implement the ImapClient class. """

import imaplib

__all__ = [ "ImapClient" ]

class ImapClient:

    """ This class is a imap client to receive email. """

    def __init__(
        self, server="", port=None, username=None, password=None, ssl=True, debug=0
    ):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        if ssl and not port:
            self.port = imaplib.IMAP4_SSL_PORT
        elif not ssl and not port:
            self.port = imaplib.IMAP4_PORT
        self.ssl = ssl
        self.debug = debug

    def create_connection(self):

        """ This method make imap client and authentication. """

        if self.ssl:
            self.mailserver = imaplib.IMAP4_SSL(self.server, self.port)
            if self.debug:
                self.mailserver.debug = self.debug
        else:
            self.mailserver = imaplib.IMAP4(self.server, self.port)
            if self.debug:
                self.mailserver.debug = self.debug
        self.mailserver.login(self.username, self.password)

    def end_connection(self):

        """ This method close imap client and connection. """

        self.mailserver.close()
        self.mailserver.logout()

    def get_all_mail(self, reverse=False):

        """ This method is a generator to get all emails. """

        self.create_connection()
        self.mailserver.select()
        response_error, emails = self.mailserver.search(None, "ALL")

        ids = emails[0].split()
        lenght = len(emails[0].split())

        if reverse:
            ids.reverse()

        for i, id_ in enumerate(ids):
            yield lenght, i, self.mailserver.fetch(id_, "(RFC822)")[1][0][1]

        self.end_connection()
