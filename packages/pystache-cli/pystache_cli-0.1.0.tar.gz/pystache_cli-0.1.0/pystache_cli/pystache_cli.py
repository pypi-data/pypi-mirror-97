#!/usr/bin/env python3
import os
import logging
import argparse
import json

import pystache

LOG_FMT = "[%(asctime)s %(levelname)7s] %(message)s"


def render(
    output_file,
    template_file,
    context_file,
    file_encoding,
    partial_file_extension,
    partial_paths,
    strict,
):
    # read template
    with open(template_file, encoding=file_encoding) as file:
        template = file.read()

    # read context
    if context_file:
        with open(context_file, encoding=file_encoding) as file:
            context = json.load(file)
    else:
        context = {}

    if not partial_file_extension:
        # use same as template file
        _, partial_file_extension = os.path.splitext(template_file)
        partial_file_extension = partial_file_extension.strip(".")

    # run pystache and save result
    renderer = pystache.Renderer(
        file_encoding=file_encoding,
        search_dirs=partial_paths,
        file_extension=partial_file_extension,
        missing_tags="strict" if strict else "ignore",  # raise error on missing tags
    )
    result = renderer.render(template, context)
    with open(output_file, "w", encoding=file_encoding) as file:
        file.write(result)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--loglevel",
        "-l",
        default="info",
        choices=["debug", "info", "warning", "error"],
    )
    ap.add_argument("output_file", help="filepath to save output")
    ap.add_argument("template_file", help="filepath to input template")
    ap.add_argument("--context_file", "-c", help="optional filepath to context json")
    ap.add_argument("--partial_paths", "-p", nargs="*")
    ap.add_argument("--partial_file_extension", "-x", default="")
    ap.add_argument("--file_encoding", "-e", default="utf-8")
    ap.add_argument(
        "--strict",
        "-s",
        action="store_true",
        help="if set: raise exception on missing keys",
    )
    kwargs = vars(ap.parse_args())
    loglevel = getattr(logging, kwargs.pop("loglevel").upper())
    logging.basicConfig(format=LOG_FMT, level=loglevel)
    render(**kwargs)


if __name__ == "__main__":
    main()
