#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################
#    This file implement the Forger class.
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

""" This file implement the Forger class. """

from email.mime.multipart import MIMEMultipart
from email.encoders import encode_base64
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from datetime import datetime
from os import path
import email.utils

try:
    from .Email import Email
except ImportError:
    from Email import Email

__all__ = [ "Forger", "main" ]

class Forger(Email):

    """ This class can forge an email. """

    def __init__(
        self,
        mail,
        titre: str = None,
        pseudo: str = None,
        comments: str = None,
        keywords: list = None,
        date: datetime = datetime.now(),
        encrypted: str = None,
        expires: datetime = None,
        importance: int = 0,
        sensitivity: int = 0,
        language: list = None,
        priority: int = 0,
        add_from: bool = False,
        default_text: str = "Your mailer can't read this email."
    ):
        super().__init__()
        if pseudo:
            self.sender = f"{pseudo} <{mail}>"
        else:
            self.sender = mail

        if expires:
            self.expires = email.utils.format_datetime(expires)
        else:
            self.expires = None

        if importance == 1:
            self.importance = "low"
        elif importance == 2:
            self.importance = "normal"
        elif importance == 3:
            self.importance = "hight"
        else:
            self.importance = None

        if sensitivity == 1:
            self.sensitivity = "Personal"
        elif sensitivity == 2:
            self.sensitivity = "Private"
        elif sensitivity == 3:
            self.sensitivity = "Company-Confidential"
        else:
            self.sensitivity = None

        if priority == 1:
            self.priority = "non-urgent"
        elif priority == 2:
            self.priority = "normal"
        elif priority == 3:
            self.priority = "urgent"
        else:
            self.priority = None

        self.address.append(mail)
        self.recipients = []
        self.id = 0
        self.comments = comments
        self.encrypted = encrypted
        self.add_from = add_from
        if language:
            self.language = ", ".join(language)  # fr, en
        else:
            self.language = None
        if keywords:
            self.keywords = ", ".join(keywords)
        else:
            self.keywords = None
        self.titre = titre
        self.date = email.utils.format_datetime(date)
        self.email = MIMEMultipart(
            "alternative"
        )  # can send more than one message

        self.add_part(default_text)

    def add_part(self, text, content="plain", add=True):

        """ This method add a part in email. """

        if add:
            part = MIMEText(text, content, _charset="utf-8")
            self.email.attach(part)
            self.part[f"part-{hex(self.id)}.{content}"] = part.get_payload(
                decode=True
            ).decode()
            self.id += 1
        else:
            return MIMEText(text, content, _charset="utf-8")

    def add_image(self, filename, html):

        """This method add part in email with image (this image isn't a attachment).
        This image must be inside HTML code."""

        part = MIMEMultipart(
            "related"
        )  # can send more than one message and attach image
        html_part = self.add_part(
            html.replace("[image]", f'<img src="cid:image{hex(self.id)}">'),
            "html",
            add=False,
        )

        with open(filename, "rb") as image:
            binary = image.read()

        self.binary[filename] = binary
        attach_image = MIMEImage(binary)
        attach_image.add_header("Content-ID", f"<image{hex(self.id)}>")

        part.attach(html_part)
        part.attach(attach_image)

        self.part[filename] = attach_image.get_payload()
        self.part[f"part-{hex(self.id)}.html"] = html_part.get_payload(
            decode=True
        ).decode()
        self.email.attach(part)
        self.id += 1

    def add_attachement(self, filename):

        """ This method add part attachment in email. """

        email = MIMEMultipart("mixed") # Multipart with email + attachement
        email.attach(self.email)

        part = MIMEBase(
            "application",
            f'octet-stream; name="{path.basename(filename)}"',
            _charset="utf-8",
        )
        part.add_header(
            "Content-Disposition", f'attachment; filename="{path.basename(filename)}"'
        )
        with open(filename, "rb") as file:
            binary = file.read()

        self.binary[filename] = binary
        part.set_payload(binary)
        encode_base64(part)
        try:
            self.attachements[filename] = part.get_payload(decode=True).decode()
        except UnicodeDecodeError:
            self.attachements[filename] = part.get_payload()
        email.attach(part)

        self.email = email

    def add_recipient(self, email):

        """ This method add a receiver address. """

        email = self.check_email(email)
        if email and isinstance(email, str):
            self.address.append(email)
            self.recipients.append(email)
        else:
            return "ERROR : email is not valid, please add a valid email."

    def make_email(self):

        """ This method build the email message. """

        self.email["Sender"] = self.sender
        if self.add_from :
            self.email["From"] = self.sender
        self.email["Date"] = self.date
        if self.comments:
            self.email["Comments"] = self.comments
        if self.keywords:
            self.email["Keywords"] = self.keywords
        if self.encrypted:
            self.email["Encrypted"] = self.encrypted
        if self.expires:
            self.email["Expires"] = self.expires
        if self.language:
            self.email["Language"] = self.language
        if self.importance:
            self.email["Importance"] = self.importance
        if self.sensitivity:
            self.email["Sensitivity"] = self.sensitivity
        if self.priority:
            self.email["Priority"] = self.priority
        if self.titre:
            self.email["Subject"] = self.titre
        self.email["To"] = ", ".join(self.recipients)


def parse():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("sender", help="The sender address.")
    parser.add_argument(
        "--pseudo", "-p", help='The sender "printable name".', default=None
    )
    parser.add_argument("--title", "-t", help="The email subject.", default=None)
    parser.add_argument("--comments", "-c", help="Email comments.", default=None)
    parser.add_argument(
        "--keywords",
        "-k",
        help='Email keywords (example : "test,email").',
        default=None,
    )
    parser.add_argument(
        "--datetime",
        "-d",
        help='Sending date. (example : "2020-12-10 11:20:02")',
        default=None,
    )
    parser.add_argument("--encrypted", "-e", help="Encrypted header.", default=None)
    parser.add_argument(
        "--expires",
        "-E",
        help='Expiration date. (example : "2021-12-10 11:20:03")',
        default=None,
    )
    parser.add_argument(
        "--importance", "-i", help="Email importance", choices=[1, 2, 3], default=0, type=int
    )
    parser.add_argument(
        "--sensitivity", "-s", help="Email sensitivity", choices=[1, 2, 3], default=0, type=int
    )
    parser.add_argument(
        "--priority", "-r", help="Email priority", choices=[1, 2, 3], default=0, type=int
    )
    parser.add_argument(
        "--language", "-l", help='Email language (example : "en,fr,it").', default=None
    )
    parser.add_argument(
        "--to",
        "-T",
        help='Address visible in email (as receivers) (example : "reply@example.com,a@example.com,victim@example.com").',
        default="",
    )
    parser.add_argument("--message", "-m", help="Email message.", default=None)
    parser.add_argument(
        "--messageHTML", "-H", help="Email message as HTML.", default=None
    )
    parser.add_argument(
        "--attachment",
        "-a",
        help="Email attachment (value : the attachment filename).",
        default=None,
    )
    parser.add_argument("--savein", "-S", help="Filename to save email.", default=None)
    parser.add_argument(
        "--smtp", "-M", help="SMTP server to send the mail.", default=None
    )
    parser.add_argument(
        "--port",
        "-O",
        help="Port of the SMTP server to send the mail (25, 465, 587).",
        default=25,
        type=int,
    )
    parser.add_argument(
        "--username",
        "-U",
        help="Username use to login on the SMTP server.",
        default=None,
    )
    parser.add_argument(
        "--password",
        "-P",
        help="Password use to login on the SMTP server.",
        default=None,
    )
    parser.add_argument(
        "--receivers", "-R", help="Real receivers (not visible in mail).", default=None
    )
    parser.add_argument(
        "--user",
        "-N",
        help="User used to send email (if you send an email i recommend you to use this option).",
        default=None,
    )
    parser.add_argument(
        "--usetls",
        "-L",
        help="Use TLS to send your email.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--debugconnection",
        "-D",
        help="Verbosity level for SMTP client.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--add_from",
        "-F",
        help="Add the FROM header (some SMTP server send an error 554 with this error).",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--ehlo",
        "-A",
        help="Machine name to send to the server with ehlo command.",
        default="PyEmailTools",
    )
    parser.add_argument(
        "--default-text",
        "-x",
        help="Default text if HTML can't be read by mailer.",
        default="Your mailer can't read this email.",
    )
    return parser.parse_args()


def format_parser(parser):
    if parser.keywords:
        parser.keywords = parser.keywords.split(",")
    if parser.language:
        parser.language = parser.language.split(",")
    if parser.to:
        parser.to = parser.to.split(",")
    if parser.datetime:
        parser.datetime = datetime.strptime(parser.datetime, "%Y-%m-%d %H:%M:%S")
    else:
        parser.datetime = datetime.now()
    if parser.expires:
        parser.expires = datetime.strptime(parser.expires, "%Y-%m-%d %H:%M:%S")
    if not parser.user and parser.smtp:
        if parser.username:
            parser.user = parser.username
        else:
            parser.user = parser.sender
    if parser.receivers:
        parser.receivers = parser.receivers.split(",")
    return parser


def main():
    try:
        from .SmtpClient import SmtpClient
    except ImportError:
        from SmtpClient import SmtpClient

    parser = format_parser(parse())
    email = Forger(
        parser.sender,
        titre=parser.title,
        pseudo=parser.pseudo,
        comments=parser.comments,
        keywords=parser.keywords,
        date=parser.datetime,
        encrypted=parser.encrypted,
        expires=parser.expires,
        importance=parser.importance,
        sensitivity=parser.sensitivity,
        language=parser.language,
        priority=parser.priority,
        add_from=parser.add_from
    )

    for receiver in parser.to:
        email.add_recipient(receiver)

    if parser.messageHTML:
        email.add_part(parser.messageHTML, "html")

    if parser.message:
        email.add_part(parser.message, "plain")

    if parser.attachment:
        email.add_attachement(parser.attachment)

    email.make_email()

    if parser.savein:
        email.save_in_file(parser.savein)

    if parser.smtp:
        smtpclient = SmtpClient(
            parser.smtp,
            parser.port,
            parser.username,
            parser.password,
            parser.usetls,
            False,
            parser.debugconnection,
        )
        smtpclient.send(email, parser.user, parser.receivers, parser.ehlo)


if __name__ == "__main__":
    main()
