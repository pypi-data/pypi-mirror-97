#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This package implement a Web Site Cloner 
and his HTTP server to launch it. """

###################
#    This package implement a Web Site Cloner and his HTTP server to launch it.
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

from sys import argv
from os import path

try:
    from .WebSiteCloner import main as cloner
    from .HTTPLogger import main as server
except ImportError:
    from WebSiteCloner import main as cloner
    from HTTPLogger import main as server

if len(argv) > 1:
    function = argv.pop(1).lower()
    if function == "cloner":
        cloner()
        exit(0)
    elif function == "server":
        server()
        exit(0)

print(
    """
WebSiteCloner  Copyright (C) 2021  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
)

print(f"""USAGES: 
    {path.basename(argv[0])} server
    {path.basename(argv[0])} cloner
HELP:
    {path.basename(argv[0])} cloner --help
    {path.basename(argv[0])} server -h
""")