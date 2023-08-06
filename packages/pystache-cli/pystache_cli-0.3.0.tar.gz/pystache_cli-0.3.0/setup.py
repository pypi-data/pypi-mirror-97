import re
from setuptools import setup, find_packages

import pystache_cli as pkg

if __name__ == "__main__":

    with open("README.md", encoding="utf-8") as file:
        long_description = file.read()

    setup(
        packages=find_packages(),
        keywords=["cli", "pystache", "template"],
        install_requires=["pystache"],
        extras_require={
            "dev": ["black", "bumpversion", "pip", "twine", "setuptools", "nose"]
        },
        name=pkg.__name__,
        description=re.sub("\s+", " ", pkg.__doc__).strip(),  # should be one line
        long_description=long_description,
        long_description_content_type="text/markdown",  # text/markdown or text/x-rst or text/plain
        version=pkg.__version__,
        author=pkg.__author__,
        author_email=pkg.__email__,
        maintainer=pkg.__author__,
        maintainer_email=pkg.__email__,
        url=pkg.__url__,
        download_url=pkg.__url__,
        platforms=["any"],
        license="Public Domain",
        project_urls={"Bug Tracker": pkg.__url__,},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
            "Operating System :: OS Independent",
        ],
        entry_points={
            "console_scripts": ["pystache-cli = pystache_cli.pystache_cli:main"]
        },
        package_data={"tests": ["data/**"]},
    )
