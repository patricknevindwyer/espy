## Check Your Environment

Create a file called _Pyfile_ in the root of your project, and annotate what libraries and external commands you need to have installed:

    python > 2.7
	ext pip >= 1.0
	pylib pymongo > 2.1.0
	ext mongod >= 2.0.0

Run espy, and see if your corner of the world is sane:

    > espy
	Python >= 2.7 ... ok
	pip >= 1.0 ... ok
	pymongo >= 2.1.0 ... ok
	mongod >= 2.0.0 ... ok
	====================
	Vefiried 4 of 4.
	++ Environment Passed

So long as the library or external command loosely comply with [SEMVER](http://semver.org/), Espy will do it's best to parse the version, and compare. And real life means more than one language in a development stack, so Espy is extentable to include new version checkers as life gets in the way.

Espy currently supports:

  * Python Version
  * Python Libraries
  * External Commands
