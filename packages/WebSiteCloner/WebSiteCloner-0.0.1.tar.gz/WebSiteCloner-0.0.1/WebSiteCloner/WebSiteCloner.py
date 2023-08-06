#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This script implement a the WebSite Cloner with
GetURLsFromHTML class and WebSiteCloner class. """

###################
#    This script implement a the WebSite Cloner with GetURLsFromHTML class and WebSiteCloner class.
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

from urllib.parse import urlparse, ParseResult
from urllib.error import URLError, HTTPError
from http.client import HTTPResponse
from argparse import ArgumentParser
from html.parser import HTMLParser
from urllib.request import urlopen
from typing import List, Tuple
from os import path, makedirs
from re import match
import logging


class UrlError(ValueError):
    pass


class GetURLsFromHTML(HTMLParser):

    """ This class get URLs from HTML. """

    def __init__(self, master):
        super().__init__()
        self.master = master

    def handle_starttag(self, tag: str, attributes: List[Tuple[str, str]]) -> None:

        """ This function get URLs attributes and values. """

        for attribute in attributes:
            if attribute[0] in [
                "src",
                "href",
                "cite",
                "code",
                "codebase",
                "data",
                "poster",
                "srcset",
                "srcdoc",
            ]:
                if not match(
                    "^https?://(w{0,3})[.]?(([a-zA-Z-]+)[.])+[a-zA-Z]{0,5}[!\x23-\x3B=\x3F-\x5B\]_\x61-\x7A~]*$",
                    attribute[1],
                ) or match(
                    "^https?://(w{1,3})?[.]?" + self.master.urlparse.netloc + ".*$",
                    attribute[1],
                ):
                    self.master.add_new_url(attribute[1])
                else:
                    return


class WebSiteCloner:

    """ This class Clone a Page and her ressources. """

    def __init__(
        self,
        url: str,
        directory: str = "CloneWebSite",
        recursive: bool = False,
        replace_domain: str = None,
        loglevel: int = logging.INFO,
        logfile: str = None,
        replace_scheme: str = None,
    ):
        self.urlparse: ParseResult = urlparse(url)
        self.html: bytes = None
        self.html_parser: GetURLsFromHTML = GetURLsFromHTML(self)
        self.directory = directory
        self.recursive = recursive
        self.replace_domain = replace_domain.encode() if replace_domain else None
        self.urls_to_parse: List[ParseResult] = [self.urlparse.path]
        self.urls_parsed: List[ParseResult] = []
        self.loglevel = loglevel
        self.logfile = logfile
        self.replace_scheme = replace_scheme.encode() if replace_scheme else None

    def launch(self) -> None:

        """ Launcher to copy a website. """

        logging.basicConfig(
            format="%(asctime)s %(levelname)s : %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
            level=self.loglevel,
            filename=self.logfile,
        )

        first = True

        while self.urls_to_parse:
            url = self.urls_to_parse.pop()
            self.urls_parsed.append(url)

            response = self.get_data(url)

            if not response:
                continue

            is_html = "text/html" in response.getheader("content-type")
            data = response.read()

            self.write_file(
                url,
                data,
            )

            if is_html and (self.recursive or first):
                self.html_parser.feed(data.decode())
                if first:
                    first = False
            elif first and not is_html:
                logging.critical(f"URL {self.url} is not valid in this context.")
                raise UrlError(f"URL {self.url} is not valid in this context.")

    def add_new_url(self, url: str) -> None:

        """ This function add new url to parse. """

        url_parsed = urlparse(url)

        if (
            (url_parsed.netloc == self.urlparse.netloc or url_parsed.netloc == "")
            and url_parsed.path not in self.urls_to_parse
            and url_parsed.path not in self.urls_parsed
        ):
            self.urls_to_parse.append(url_parsed.path)

    def get_complete_url(self, url: str) -> str:

        """ This function build a complete url. """

        if url and url[0] == "/":
            complete_url = "https://" + self.urlparse.netloc + url
        elif self.urlparse.path != "/":
            complete_url = (
                "https://" + self.urlparse.netloc + self.urlparse.path + "/" + url
            )
        else:
            complete_url = "https://" + self.urlparse.netloc + self.urlparse.path + url

        return complete_url

    def get_data(self, url: str) -> HTTPResponse:

        """ This function return HTTP response. """

        url = self.get_complete_url(url)

        try:
            response = urlopen(url)
        except URLError:
            logging.error(
                f"This URL isn't valid. Failed to get ressources from this url: {url}"
            )
            return None
        except HTTPError as error:
            logging.error(
                f"HTTP {error.code} error. Failed to get ressources from this url : {url}"
            )
            return None

        logging.info(f"Get ressources from this URL : {url}")
        return response

    def write_file(self, url: str, data: bytes) -> bytes:

        """ This function get URL path and write the file in the good location. """

        url_parsed = urlparse(url)
        directory = self.get_directory_from_url(url, url_parsed)
        full_path = self.get_full_path(url, directory, url_parsed)

        if self.replace_domain:
            data = data.replace(self.urlparse.netloc.encode(), self.replace_domain)
        if self.replace_scheme:
            data = data.replace(self.urlparse.scheme.encode(), self.replace_scheme)

        file = open(full_path, "wb")
        file.write(data)
        file.close()

    def get_full_path(self, url: str, directory: str, url_parsed: ParseResult) -> str:

        """ This function return full path (directory + filename) to write the file. """

        filename = path.basename(url_parsed.path)
        if "." not in filename:
            directory = path.join(directory, filename)
            filename = "index.html"

        logging.debug(f"Path for URL: {url} (path: {url_parsed.path}) is {directory}")

        full_path = path.join(self.urlparse.netloc, directory)
        if path.isdir(self.directory):
            full_path = path.join(self.directory, full_path)
        if not path.exists(full_path):
            makedirs(full_path)

        logging.debug(
            f"Finally path for URL: {url} (path: {url_parsed.path}) is {full_path}"
        )

        full_path = path.join(full_path, filename)
        if path.exists(full_path):
            if path.isdir(full_path):
                full_path = path.join(full_path, "index.html")

        logging.debug(
            f"The filename for URL: {url} (path: {url_parsed.path}) is {full_path}"
        )

        return full_path

    def get_directory_from_url(self, url: str, url_parsed: ParseResult) -> str:

        """ This function return directory to write the file. """

        directory = path.normcase(path.dirname(url_parsed.path))

        logging.debug(
            f"Directory for URL: {url} (path: {url_parsed.path}) is {directory}"
        )

        if not directory or directory[0] == "/" or directory[0] == "\\":
            directory = "." + directory
        else:
            directory = path.join(path.normcase("." + self.urlparse.path), directory)

        logging.debug(
            f"Finally directory for URL: {url} (path: {url_parsed.path}) is {directory}"
        )

        return directory


def parse():
    parser = ArgumentParser()
    parser.add_argument(
        "url",
        help="URL to clone.",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        help="Copy data from all urls recursively.",
        action="store_true",
    )
    parser.add_argument(
        "--directory",
        "-d",
        help="Copy data in specific directory.",
        default="CloneWebSite",
    )
    parser.add_argument(
        "--mydomain", "-D", help="Replace domain target by custom domain.", default=None
    )
    parser.add_argument(
        "--myscheme", "-S", help="Replace scheme target by custom scheme.", default=None
    )
    parser.add_argument(
        "--loglevel",
        "-l",
        help="WebSiteCloner logs level.",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.add_argument(
        "--logfile", "-f", help="WebSiteCloner logs file.", default=None
    )
    return parser.parse_args()


def main():
    args = parse()

    copy: WebSiteCloner = WebSiteCloner(
        args.url,
        recursive=args.recursive,
        directory=args.directory,
        replace_domain=args.mydomain,
        replace_scheme=args.myscheme,
        loglevel=logging.__dict__[args.loglevel],
        logfile=args.logfile,
    )
    copy.launch()


if __name__ == "__main__":
    main()
