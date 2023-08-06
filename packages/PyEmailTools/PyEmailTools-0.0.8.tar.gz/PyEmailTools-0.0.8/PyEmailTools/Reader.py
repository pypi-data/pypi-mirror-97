#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################
#    This file implement the Reader class.
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

""" This file implement the Reader class. """

from email.parser import BytesParser
from email.policy import default
from fnmatch import fnmatch
from re import finditer
import mimetypes

try:
    from .Email import Email, Constantes
except ImportError:
    from Email import Email, Constantes

__all__ = [ "Reader", "main" ]

class Reader(Email):

    """This class read eml file, parse the mail and extract information."""

    def __init__(self, filename=None):
        super().__init__()
        self.file = filename
        self.email = None

    def make_email(self, email: bytes = None):

        """ This method parse email bytes and get important informations for analysis. """

        if not email:
            email_file = open(self.file, "rb")
            self.email = BytesParser().parse(email_file)
            email_file.close()
        else:
            self.email = BytesParser().parsebytes(email)

        for address in finditer(Constantes.REGEX_EMAIL.value, str(self.email)):
            self.address.append(address.group().strip())

        for ip in finditer("([0-9]{1,3}[.]){3}[0-9]{1,3}", str(self.email)):
            self.ips.append(ip.group())

        for ip in finditer(
            "\[IPv6[:]([0-9a-f]{1,4}[:]{1,2}){1,7}[0-9a-f]{0,4}\]", str(self.email)
        ):
            self.ips.append(ip.group())

        for header in self.email._headers:
            self.headers.setdefault(header[0], []).append(header[1])

        self.get_part()

    def get_part(self):

        """ This method parse part in email. """

        id_ = 0

        for part in self.email.walk():
            id_ += 1
            disposition = part.get("Content-Disposition")
            if disposition:
                disposition = disposition.split(";")

            if part.get_content_maintype() == "multipart":
                continue
            elif disposition and "attachment" in disposition:
                filename = self.get_part_name(part, id_)
                self.attachements[f"{filename} :: {id_}"] = self.get_part_payload(
                    part, filename, id_
                )
            else:
                filename = self.get_part_name(part, id_)
                self.part[f"{filename} :: {id_}"] = self.get_part_payload(
                    part, filename, id_
                )

    def get_part_payload(self, part, filename, id_):

        """ This method decode email payload. """

        payload = part.get_payload(decode=True)
        if payload:
            try:
                payload = payload.decode(part.get_content_charset(failobj="utf-8"))
            except UnicodeDecodeError:
                payload = part
                self.binary[f"{filename} :: {id_}"] = part.get_payload(decode=True)
        else:
            payload = ""
        return payload

    def get_part_name(self, part, id_):

        """ This method get the name of a part. """

        filename = part.get_filename()
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                ext = ".bin"
            filename = f"part-{id_}{ext}"
        return filename

    def research(
        self,
        pattern: str,
        regex: bool = False,
        keep_uppercase: bool = False,
        glob: bool = False,
    ):

        """ This method research pattern in email data and decoded part. """

        if regex:
            for match in finditer(pattern, self.email.as_string()):
                yield match.group()
            for name, part in self.part.items():
                if name not in self.binary.keys():
                    for match in finditer(pattern, part):
                        yield match.group()

        elif keep_uppercase:
            yield from find_in_string_and_list(
                pattern, self.email.as_string(), self.part.values()
            )
        elif glob and fnmatch(self.email.as_string(), pattern):
            yield pattern

        elif glob:
            for name, part in self.part.items():
                if name not in self.binary.keys():
                    if fnmatch(part, pattern):
                        yield pattern

        else:
            yield from find_in_string_and_list(
                pattern.lower(),
                self.email.as_string().lower(),
                [part.lower() for part in self.part.values()],
            )


def find_in_string_and_list(pattern, string, list_):
    if pattern in string:
        yield pattern
    for part in list_:
        if pattern in part:
            yield pattern


def parse():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "--regex",
        "-K",
        help="Use the research option as regular expression.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--print",
        "-p",
        help="Print email in terminal/console (with different verbosity level).",
        default=0,
        type=int,
        choices=range(1, 5),
    )
    parser.add_argument(
        "--keepupper",
        "-k",
        help="Keep uppercase and lowercase.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--globresearch",
        "-B",
        help="Use glob patterns in research (Example : te*@gmail.com,@*.net).",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--research",
        "-s",
        help='Research value in emails (Example : "gmail.com").',
        default=None,
    )
    parser.add_argument(
        "--reverseorder",
        "-R",
        help="Reverse the order to get emails.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--requestnumber",
        "-r",
        help="Number of request to send to the server.",
        type=int,
        default=0
    )
    parser.add_argument(
        "--limit", "-l", help="Limit the number of email to get.", type=int, default=0
    )
    parser.add_argument(
        "--haveheader", "-H", help="Get all mail with this header.", default=None
    )
    parser.add_argument(
        "--haveheadervalue",
        "-v",
        help="Get all mail with this header and value (this option use the haveharder option).",
        default=None,
    )
    parser.add_argument(
        "--getheader",
        "-g",
        help="Get all values of this header in emails.",
        default=None,
    )
    parser.add_argument(
        "--files",
        "-f",
        help="EML files with glob pattern for analysis (Example : 01.eml,02.eml).",
        default=None,
    )
    parser.add_argument(
        "--globfiles",
        "-G",
        help="Use glob pattern for filenames (Example : mail*.eml,file*.eml,/home/*.eml).",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--ip",
        "-i",
        help="Print all IP address.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--address",
        "-a",
        help="Print all email address.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--savein",
        "-S",
        help="Basename to save email (Example : mail -> mail1.eml, mail2.eml...).",
        default=None,
    )
    parser.add_argument(
        "servertype",
        help="Server type to get emails.",
        choices=["imap", "pop3", "files"],
    )
    parser.add_argument(
        "--servername",
        "-N",
        help="Server name to get emails.",
    )
    parser.add_argument(
        "--port",
        "-O",
        help="IMAP/POP3 port to get emails.",
        default=None,
        type=int,
    )
    parser.add_argument(
        "--username",
        "-U",
        help="Username use to login on the IMAP/POP3 server.",
        default=None,
    )
    parser.add_argument(
        "--password",
        "-P",
        help="Password use to login on the IMAP/POP3 server.",
        default=None,
    )
    parser.add_argument(
        "--usetls",
        "-L",
        help="Use TLS to send your email (i recommended this options for all connections).",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--debugconnection",
        "-D",
        help="Verbosity level fort IMAP/POP3 client.",
        default=False,
        action="store_true",
    )
    return parser.parse_args()


def get_imap_client(parser):
    try:
        from .ImapClient import ImapClient
    except ImportError:
        from ImapClient import ImapClient

    return ImapClient(
        server=parser.servername,
        port=parser.port,
        username=parser.username,
        password=parser.password,
        ssl=parser.usetls,
        debug=4 if parser.debugconnection else 0,
    )


def get_pop3_client(parser):
    try:
        from .PopClient import PopClient
    except ImportError:
        from PopClient import PopClient

    return PopClient(
        parser.servername,
        parser.port,
        parser.username,
        parser.password,
        parser.usetls,
        4 if parser.debugconnection else 0,
    )


def build_email(data):
    email = Reader()
    try:
        email.make_email(data)
    except Exception as e:
        print(f"InvalidEmail: {e}")
    else:
        return email


def find_in(list1, list2):
    for value in list1:
        if value not in list2:
            list2.append(value)
            yield value, list2


def process_email(parser, email, address, ip, header, emails, index):
    if parser.address:
        for email_address, address in find_in(email.address, address):
            print(f"\tNew Email Address found : {email_address}")

    if parser.ip:
        for ip_address, ip in find_in(email.ips, ip):
            print(f"\tNew IP Address found : {ip_address}")

    if parser.getheader:
        value = email.headers.get(parser.getheader)
        if value and value not in header:
            header.append(value)
            print(f'\tNew value found for header "{parser.getheader}" : {value}')

    if parser.research:
        for pattern in email.research(
            parser.research, parser.regex, parser.keepupper, parser.globresearch
        ):
            emails.append(email)
            break

    if parser.haveheader and email not in emails:
        value = email.headers.get(parser.haveheader)
        if value and parser.haveheadervalue and value == parser.haveheadervalue:
            emails.append(email)
        elif value and not parser.haveheadervalue:
            emails.append(email)

    if (email in emails) or (not parser.research and not parser.haveheader):
        if parser.savein:
            print("\t[!]", end=" ")
            email.save_in_file(f"{parser.savein}{index}.eml")

        if parser.print == 1:
            email.print()
        elif parser.print == 2:
            email.print(part=True)
        elif parser.print == 3:
            email.print(part=True, attachements=True)
        elif parser.print == 4:
            email.print(part=True, attachements=True, email=email.email)

    print("")
    return address, ip, header, emails


def get_emails(parser, client=None):
    if client:
        yield from client.get_all_mail(parser.reverseorder)
    elif parser.servertype == "files":
        yield from get_data_from_files(parser)


def get_filenames(parser):
    from glob import glob

    patterns = parser.files.split(",")
    lenght = len(patterns)
    for i, pattern in enumerate(patterns):
        if parser.globfiles:
            files = glob(pattern)
            lenght = len(files)
            for i_, file in enumerate(files):
                yield lenght, i_, file
        else:
            yield lenght, i, pattern


def get_data_from_files(parser):
    for lenght, i, filename in get_filenames(parser):
        with open(filename, "rb") as file:
            yield lenght, i, file.read()


def main():
    from getpass import getpass
    parser = parse()

    address = []
    ip = []
    header = []
    emails = []
    request_number = 0

    client = None
    if parser.servertype == "imap":
        if not parser.password:
            parser.password = getpass()
        client = get_imap_client(parser)
    elif parser.servertype == "pop3":
        if not parser.password:
            parser.password = getpass()
        client = get_pop3_client(parser)

    for lenght, i, mail in get_emails(parser, client):
        print(
            f"Processing email {i} / {parser.requestnumber if parser.requestnumber else lenght}"
        )
        email = build_email(mail)
        if email:
            address, ip, header, emails = process_email(
                parser, email, address, ip, header, emails, request_number
            )

        request_number += 1
        if parser.limit and len(emails) >= parser.limit:
            break

        if parser.requestnumber and request_number >= parser.requestnumber:
            break


if __name__ == "__main__":
    main()
