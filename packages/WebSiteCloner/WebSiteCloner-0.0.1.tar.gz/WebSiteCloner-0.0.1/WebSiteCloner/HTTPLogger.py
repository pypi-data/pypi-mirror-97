#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This script implement a HTTP Logger class to launch
cloned WebSite and save the requests. """

###################
#    This script implement a HTTP Logger class to launch cloned WebSite and save the requests.
#    Copyright (C) 2021  Maurice Lambert

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

from http.server import HTTPServer, SimpleHTTPRequestHandler
from argparse import ArgumentParser
from os import path, chdir
import logging


class HTTPLogger(SimpleHTTPRequestHandler):

    """This class is basic HTTP Server to launch a cloned WebSite.
    This class log the request and data sending with it (credentials, secret files...)."""

    def do_GET(self, data=None) -> None:

        """ This function log HTTP GET request and return the file. """

        self.sys_version = ""
        self.server_version = CONSTANTES.HEADER_SERVER

        logging.info(
            f'{self.client_address} asking "{self.command} {self.path}" on {self.headers.get("Host")}'
        )

        headers_string = ""
        for header, value in self.headers.items():
            headers_string += f"{header}:{value}; "

        logging.info(f"Headers sending by {self.client_address}: {headers_string}")

        if data:
            logging.info(f"Data sending by {self.client_address}: {data}")

        SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self) -> None:

        """ This function get data from HTTP POST request. """

        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        self.do_GET(data=post_data)

    def end_headers(self) -> None:

    	""" This function send custom headers and call the real end_headers function. """

    	for header, value in CONSTANTES.HEADERS:
    		self.send_header(header, value)

    	SimpleHTTPRequestHandler.end_headers(self)


class CONSTANTES:

    """ Constantes class for permanent HTTP server values. """

    HEADER_SERVER = "WebSiteCloner"
    LOGFILE = None
    LOGLEVEL = logging.DEBUG
    DIRECTORY = "CloneWebSite"
    HEADERS = []
    PORT = 80
    INTERFACE = "0.0.0.0"


def parse():
    parser = ArgumentParser()
    parser.add_argument(
        "domain",
        help="Domain cloned or directory.",
    )
    parser.add_argument("--logfile", "-f", help="HTTP server logs file.", default=None)
    parser.add_argument(
        "--headers",
        "-H",
        help="Additionnal headers for response with this format: name:value,name:value... (Server:Apache).",
        default=None,
    )
    parser.add_argument(
        "--server", "-S", help="Server header.", default="WebSiteCloner"
    )
    parser.add_argument(
        "--port", "-P", help="Port to launch server.", default=80, type=int
    )
    parser.add_argument(
        "--interface", "-I", help="Interface to launch server.", default="0.0.0.0"
    )
    return parser.parse_args()


def main():
    args = parse()

    if args.headers:
        for header in args.headers.split(","):
            CONSTANTES.HEADERS.append(tuple(header.split(":", 1)))

    CONSTANTES.HEADER_SERVER = args.server
    CONSTANTES.PORT = args.port
    CONSTANTES.INTERFACE = args.interface
    CONSTANTES.LOGFILE = args.logfile

    build_path = path.join(CONSTANTES.DIRECTORY, args.domain)

    if path.isdir(args.domain):
        chdir(args.domain)
        CONSTANTES.DIRECTORY = args.domain
    elif path.isdir(build_path):
        chdir(build_path)
        CONSTANTES.DIRECTORY = build_path
    else:
        logging.critical(f"{args.domain} and {build_path} are not a directory.")
        exit(2)

    logging.basicConfig(
        format='[%(asctime)s] "%(message)s"',
        datefmt="%m/%d/%Y %H:%M:%S",
        level=CONSTANTES.LOGLEVEL,
        filename=CONSTANTES.LOGFILE,
    )

    with HTTPServer((CONSTANTES.INTERFACE, CONSTANTES.PORT), HTTPLogger) as httpd:
        logging.info(f"Server is running in : {CONSTANTES.DIRECTORY}")
        logging.info(f"Server is running on : {CONSTANTES.INTERFACE}:{CONSTANTES.PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            exit(0)


if __name__ == "__main__":
    main()