#!/usr/bin/python
from distutils.core import setup
setup(
    name = "espy",
    packages = ["espy", "espy.processor", "espy.syntax"],
    scripts = ['bin/espy'],
    version = "0.4.1",
    description = "Operating Environment Inspection",
    author = "Patrick Nevin Dwyer",
    author_email = "patricknevindwyer@gmail.com",
    url = "https://github.com/patricknevindwyer/espy",
    download_url = "https://github.com/patricknevindwyer/espy/tarball/master",
    keywords = ["library", "environment", "validate"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities"
        ],
    long_description = """\
Operating Environment Inspection
-------------------------------------

Espy is a simple way to check the environment in which your code will run:

    # Boiler plate sanity check
    
    python >= 2.7
    
    # Make sure we have MongoDB and Drivers
    
    py pymongo >= 2.1.0
    
    cmd mongod >= 2.0.0
    
    # Track down Solaris GCC install
    
    cmd /usr/sfw/bin/gcc >= 4.0

Espy makes it easy to check Python Modules and external commands.
"""
)