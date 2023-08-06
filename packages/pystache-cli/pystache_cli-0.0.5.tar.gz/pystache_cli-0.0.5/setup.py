from setuptools import setup

import pystache_cli as pkg

if __name__ == "__main__":

    with open("README.md", encoding="utf-8") as file:
        long_description = file.read()

    setup(
        packages=[pkg.__name__],
        install_requires=[
            "pystache"
        ],
        name=pkg.__name__,
        description=pkg.__doc__.replace('\n', ' '),  # should be one line
        long_description=long_description,
        long_description_content_type="text/markdown",  # text/markdown or text/x-rst or text/plain
        version=pkg.__version__,
        author=pkg.__author__,
        author_email=pkg.__email__,
        url=pkg.__url__,
        project_urls={
            "Bug Tracker": pkg.__url__,
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        entry_points={
            "console_scripts": ["pystache-cli = pystache_cli.pystache_cli:main"]
        },
        package_data={
            # 'package.module: [file_patterns]'  # better to use MANIFEST.in
        },
    )
