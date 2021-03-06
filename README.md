# Check Your Environment

Create a file called _Reqfile_ in the root of your project, and annotate what libraries and external commands your project requires:

```python
	# Boiler plate checks
	python >= 2.7
	cmd pip >= 1.0

	# Check for our Python modules
	py pymongo >= 2.1
	py espy >= 0.1.0

	# Check for external commands
	cmd mongod >= 2.0.0
	cmd perl >= 5.7.1

	# Check a few ruby gems
	gem actionpack > 2.2.0
	gem mysql > 2.8
	npm mongoose > 2.5

	# Check for some perl modules
	pl CGI > 3.4
	pl Date::Calc >= 6.0

```

Run _espy_, and see if your corner of the world is sane:

```bash
    > espy
	
	External Command checks
	-----------------------
	pip >= 1.0 ... ok
	mongod >= 2.0.0 ... ok
	perl >= 5.7.1 ... ok

	Ruby Gem checks
	---------------
	actionpack > 2.2.0 ... ok
	mysql > 2.8 ... ok

	Node.js Module checks
	---------------------
	mongoose > 2.5 ... ok

	Perl Module checks
	------------------
	CGI > 3.4 ... ok
	Date::Calc >= 6.0 ... ok

	Python Module checks
	--------------------
	pymongo >= 2.1 ... ok
	espy >= 0.1.0 ... ok

	CPython Runtime checks
	----------------------
	Python >= 2.7 ... ok

	====================
	Vefiried 11 of 11.
	++ Environment Passed
```

So long as the library or external command loosely comply with [Semantic Versioning](http://semver.org/), _espy_ will do it's best to parse the version, and compare. And real life means more than one language in a development stack, so _espy_ is extentable to include new version checkers as life gets in the way.

Espy currently supports:

  * Python Version
  * Python Libraries
  * Ruby Libraries (via Gem)
  * Node.js Libraries (via NPM)
  * Perl Modules
  * External Commands

## Install

	pip install espy

## Python Version

Checking the currently active version of Python as easy as:
    
	python >= 2.6.1

The Python checker supports a semantic version of either _2 or 3_ digits, so a sanity check for Python 3 could be:

	python >= 3.0

## Python Libraries

The easiest way to check for a specific version of a Python Module is:

    py mymodule >= 1.0.0

Most Python Modules have a property called (with some variation in capitalization) _Version_. If _espy_ can find a version property in the Python Module, it will automatically check that property when doing version comparisons. If the python module you want to check _doesn't_ have a _version_ property, you can explicitly tell _espy_ what property to check instead:

	py foobaz[MyVer] == 0.9.3

In this case, _espy_ will check the _MyVer_ property of the _foobaz_ module.

The Python Library checker supports a semantic version of either _2 or 3_ digits.

## Ruby Gem Libraries

Quick and easy Gem check:

	gem mygem > 2.0

_espy_ will check against all of the installed versions that Gem can find. Semantic versions of either _2 or 3_ digits are supported.

## Node.js Libraries

Check installed Node.js libraries via NPM:

	npm myJs > 2.1.2

_espy_ will check against the local and global NPM module installation. Semantic versions with either _2 or 3_ digits are supported.

## Perl Modules

Check installed Perl modules that conform to CPAN Versioning:

	pl CGI > 3.0

_espy_ will check against the active perl installation available in the current user path. Semantic versions with either _2 or 3_ digits are supported, although most Perl modules only use the first two digits in versioning.

## External Commands

External commands are tricky things, with a multitude of command line options, verbose outputs, and line formats. In some lucky cases the external command you want to check will respond to either the _--version_ or _--help_ command line switch, in which case you don't need to do much work:

    cmd mongod > 2.0

Even though the output of the _mongod_ command might actually _look_ like:

	db version v2.0.2, pdfile version 4.5
	Sun Mar  4 15:32:13 git version: 514b122d308928517f5841888ceaa4246a7f18e3

_espy_ will look for a pattern that matches _#.#.#_, dumping the extraneous text.

If you're not lucky, and the command you want to check doesn't respond to the _--version_ or _--help_ flag, you can always specify which command line flag to use:

	cmd blarg [-h] >= 21.2.4

In most cases it's best to specify the command you want to check _without_ specifying the path; who cares where the command is installed, so long as the path works, right? Well, sometimes. But if you _do_ want to check a specific path, you can specify an exact path to an external command:

    cmd /usr/sfw/bin/gcc >= 4.6.4

The External Library checker supports a semantic version of either _2 or 3_ digits.

## Comparing Versions

_espy_ has support for basic 2 and 3 digit Semantic Versioning. Support for the full [SEMVER v1.0.0](http://semver.org/spec/v1.0.0.html) and [SEMVER v2.0.0-rc.1](http://semver.org/) are in the works. The following comparators are currently supported:

  * >
  * >=
  * =
  * !=
  * <
  * <=
  
# Contact/Comments

If you have questions, comments, rants, or requests, feel free to drop me a line.

# License

_espy_ is released under the BSD license.
