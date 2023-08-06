# Author:
# Nathan Faillenot (codejump - @c0dejump)


import pathlib

import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="HawkScan",
    version="1.7.2",
    author="c0dejump",
    author_email="codejumpgame@gmail.com",
    description="Security Tool for Reconnaissance and Information Gathering on a website. (python 2.x & 3.x)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/c0dejump/HawkScan/",
    install_requires=[
        'requests',
        'pyopenssl',
        'prettyprinter',
        'prettyprint',
        'queuelib',
        'fake_useragent',
        'python-whois',
        'argparse',
        'bs4',
        'dnspython',
        'wafw00f',
        'python-whois',
        'sockets'
    ],
    project_urls={
        "Bug Tracker": "https://github.com/c0dejump/HawkScan/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
)