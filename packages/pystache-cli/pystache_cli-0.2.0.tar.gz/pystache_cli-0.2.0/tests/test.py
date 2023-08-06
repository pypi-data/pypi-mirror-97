# coding: utf-8
import unittest
import tempfile
import logging
import os

import json

from pystache_cli import render


logging.basicConfig(
    format="[%(asctime)s %(levelname)7s] %(message)s", level=logging.DEBUG
)


def create_tmpfile(dir=None, prefix=None, suffix=None):
    """Return path to newly created, but closed tempfile."""
    tmp = tempfile.NamedTemporaryFile(
        delete=False, prefix=prefix, suffix=suffix, dir=dir
    )
    tmp.close()
    logging.debug("created: %s", os.path.abspath(tmp.name))
    return tmp.name  # actually filepath


class TestTemplate(unittest.TestCase):
    def setUp(self):
        # create closed but existing temporary file
        self.outfile = create_tmpfile(suffix=".json")
        self.datadir = os.path.join(os.path.dirname(__file__), "data")
        self.encoding = "utf-8"

    def tearDown(self):
        logging.debug("deleting: %s", os.path.abspath(self.outfile))
        os.remove(self.outfile)

    def test_json(self):
        render(
            output_file=self.outfile,
            template_file=os.path.join(self.datadir, "template.json"),
            context_file=os.path.join(self.datadir, "context.json"),
            partial_paths=[os.path.join(self.datadir, "partials")],
            file_encoding=self.encoding,
            strict=True,
            separators=[
                '"{{',
                '}}"',
            ],  # add quotation marks so pattern will be a string and stay a valid json
        )
        with open(self.outfile, encoding=self.encoding) as file:
            text = file.read()
            data = json.loads(text)
            self.assertEqual(data["value"], 100)
            self.assertEqual(len(data["list"]), 3)
