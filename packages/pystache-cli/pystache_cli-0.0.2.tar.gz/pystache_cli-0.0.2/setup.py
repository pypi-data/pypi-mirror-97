from setuptools import setup

import pystache_cli as pkg

if __name__ == "__main__":
    setup(
        packages=[pkg.__name__],
        install_requires=["pystache"],
        name=pkg.__name__,
        description=pkg.__doc__,
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
