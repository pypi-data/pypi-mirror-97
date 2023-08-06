# -*- coding: utf-8 -*-
# Created by mcwT <machongwei_vendor@sensetime.com> on 2021/02/24.

import argparse

from easy_mock import common
from easy_mock.__about__ import __description__, __version__
from easy_mock.core import main


def cli():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        '-V', '--version', dest='version', action='store_true',
        help="show version")
    parser.add_argument(
        '-p', '--port', default='9000',
        help="Port that needs mock service.")
    parser.add_argument(
        '-pb2y', '--pb-to-yaml', dest='to_yaml', default=None)
    parser.add_argument(
        '-pb2j', '--pb-to-json', dest='to_json', default=None)
    parser.add_argument('pb_source_file', nargs='?',
                        help="Need converted pb source file.")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit(0)

    if args.to_yaml or args.to_json:
        pb_source_file = args.pb_source_file
        if not pb_source_file or not pb_source_file.endswith(".proto"):
            common.log().error("pb file not specified.")
            exit(1)

        # process pb file
        exit(0)

    main(args.port)
