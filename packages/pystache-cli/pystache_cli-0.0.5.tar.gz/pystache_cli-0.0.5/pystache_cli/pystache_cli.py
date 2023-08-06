#!/usr/bin/env python3

import logging
import argparse

import pystache

LOG_FMT = "[%(asctime)s %(levelname)7s] %(message)s"


def render(
    output_file,
    template_file,
    context_file,
    file_encoding,
    partial_file_extension,
    partial_paths,
):
    # read template
    with open(template_file, encoding=file_encoding) as file:
        template = file.read()

    # read context
    if context_file:
        with open(context_file, encoding=file_encoding) as file:
            context = file.read()
    else:
        context = {}

    # run pystache and save result
    renderer = pystache.Renderer(
        file_encoding=file_encoding,
        search_dirs=partial_paths,
        file_extension=partial_file_extension,
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
    ap.add_argument("output_file")
    ap.add_argument("template_file")
    ap.add_argument("context_file", nargs="?")
    ap.add_argument("--partial_paths", "-p", nargs="*")
    ap.add_argument("--file_extension", "-x", default="")
    ap.add_argument("--file_encoding", "-e", default="utf-8")
    kwargs = vars(ap.parse_args())
    loglevel = getattr(logging, kwargs.pop("loglevel"))
    logging.basicConfig(format=LOG_FMT, level=loglevel)
    render(**kwargs)


if __name__ == "__main__":
    main()
