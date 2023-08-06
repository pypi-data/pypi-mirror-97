#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################
#    This file implement the SmtpClient.
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

""" This file implement the SmtpClient. """

import smtplib

try:
    from .Email import Email
except ImportError:
    from Email import Email

__all__ = [ "SmtpClient" ]


class SmtpClient:

    """This class send email with SMTP protocol."""

    def __init__(
        self,
        smtp=None,
        port=25,
        username=None,
        password=None,
        use_tls=True,
        use_gpg=True,
        debug=False,
    ):
        self.smtp = smtp
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.use_gpg = use_gpg
        self.debug = debug

    def send(
        self, email: Email, from_: str, to: list, name: str = "PyEmailTools"
    ) -> None:

        """ This method send an email. """

        to = self.get_valid_receivers(to + [from_], email)
        self.mailserver = smtplib.SMTP(self.smtp, self.port)
        self.mailserver.ehlo(name)
        self.mailserver.helo(name)
        if self.debug:
            self.mailserver.set_debuglevel(1)
        if self.use_tls:
            self.mailserver.starttls()
            self.mailserver.ehlo(name)
            self.mailserver.helo(name)
        if self.username and self.password:
            self.mailserver.login(self.username, self.password)
        self.mailserver.sendmail(from_, to, email.email.as_string())
        self.mailserver.quit()

    def get_valid_receivers(self, addressS, email):

        """This method return valid address.
        If address isn't valid you get a ERROR message in your console with the specific address."""

        receivers = []
        for address in addressS:
            email_ = email.check_email(address)
            if not email_ and not isinstance(email_, str):
                print(f"ERROR: this address isn't valid : {address}")
            else:
                receivers.append(address)
        return receivers
