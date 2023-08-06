import os
from setuptools import setup
from pkg_resources import parse_requirements

import pystache_cli as pkg

if __name__ == "__main__":

    path = os.path.dirname(__file__)
    with open(os.path.join(path, "README.md"), encoding="utf-8") as f:
        long_description = f.read()

    setup(
        packages=[pkg.__name__],
        install_requires=[
            "pystache"
        ],
        name=pkg.__name__,
        description=pkg.__doc__,
        long_description=long_description,
        long_description_content_type="text/markdown",  # text/markdown or text/x-rst or text/plain
        version=pkg.__version__,
        author=pkg.__author__,
        author_email=pkg.__email__,
        url=pkg.__url__,
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        entry_points={
            "console_scripts": ["pystache-cli = pystache_cli.pystache_cli:main"]
        },
        package_data={
            # 'package.module: [file_patterns]'  # better to use MANIFEST.in
        },
    )
