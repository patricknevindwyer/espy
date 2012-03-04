## Check Your Environment

Create a file called _Pyfile_ in the root of your project, and annotate what libraries and external commands your project requires:

    python > 2.7
	ext pip >= 1.0
	pylib pymongo > 2.1.0
	ext mongod >= 2.0.0

Run _espy_, and see if your corner of the world is sane:

    > espy
	Python >= 2.7 ... ok
	pip >= 1.0 ... ok
	pymongo >= 2.1.0 ... ok
	mongod >= 2.0.0 ... ok
	====================
	Vefiried 4 of 4.
	++ Environment Passed

So long as the library or external command loosely comply with [Semantic Versioning](http://semver.org/), _espy_ will do it's best to parse the version, and compare. And real life means more than one language in a development stack, so _espy_ is extentable to include new version checkers as life gets in the way.

Espy currently supports:

  * Python Version
  * Python Libraries
  * External Commands
  
## Python Version

Checking the currently active version of Python as easy as:
    
	python >= 2.6.1

The Python checker supports a semantic version of either _2 or 3_ digits, so a sanity check for Python 3 could be:

	python >= 3.0

## Python Libraries

The easiest way to check for a specific version of a Python Module is:

    pylib mymodule >= 1.0.0

Most Python Modules have a property called (with some variation in capitalization) _Version_. If _espy_ can find a version property in the Python Module, it will automatically check that property when doing version comparisons. If the python module you want to check _doesn't_ have a _version_ property, you can explicitly tell _espy_ what property to check instead:

	pylib foobaz[MyVer] == 0.9.3

In this case, _espy_ will check the _MyVer_ property of the _foobaz_ module.

The Python Library checker supports a semantic version of either _2 or 3_ digits.

## External Commands

External commands are tricky things, with a multitude of command line options, verbose outputs, and line formats. In some lucky cases the external command you want to check will respond to either the _--version_ or _--help_ command line switch, in which case you don't need to do much work:

    ext mongod > 2.0

Even though the output of the _mongod_ command might actually _look_ like:

	db version v2.0.2, pdfile version 4.5
	Sun Mar  4 15:32:13 git version: 514b122d308928517f5841888ceaa4246a7f18e3

_espy_ will look for a pattern that matches _#.#.#_, dumping the extraneous text.

If you're not lucky, and the command you want to check doesn't respond to the _--version_ or _--help_ flag, you can always specify which command line flag to use:

	ext blarg [-h] >= 21.2.4

In most cases it's best to specify the command you want to check _without_ specifying the path; who cares where the command is installed, so long as the path works, right? Well, sometimes. But if you _do_ want to check a specific path, you can specify an exact path to an external command:

    ext /usr/sfw/bin/gcc >= 4.6.4

The External Library checker supports a semantic version of either _2 or 3_ digits.

# To Write:

* comparators
* Extending
* license
* install (pip)
* example Pyfile with comments?
* espy file instead of pyfile?