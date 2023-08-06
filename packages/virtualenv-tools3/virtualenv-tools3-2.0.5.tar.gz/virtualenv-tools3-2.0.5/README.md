[![Build Status](https://travis-ci.org/Yelp/virtualenv-tools.svg?branch=master)](https://travis-ci.org/Yelp/virtualenv-tools)
[![Coverage Status](https://img.shields.io/coveralls/Yelp/virtualenv-tools.svg?branch=master)](https://coveralls.io/r/Yelp/virtualenv-tools)
[![PyPI version](https://badge.fury.io/py/virtualenv-tools3.svg)](https://pypi.python.org/pypi/virtualenv-tools3)

virtualenv-tools3
--------

virtualenv-tools3 is a fork of [the original
virtualenv-tools](https://github.com/fireteam/virtualenv-tools) (now
unmaintained) which adds support for Python 3, among other things. Full patch
details are below.

##  yelp patches

### yelp4

* Add python3 support
* Drop python2.6 support
* 100% test coverage
* Removes `$VENV/local` instead of fixing up symlinks
* Removed `--reinitialize`, instead run `virtualenv $VENV -p $PYTHON`
* Rewrite .pth files to relative paths


### yelp3

* default output much more concise, added a --verbose option
* improved fault tolerance, in the case of:
    * corrupt pyc files
    * broken symlinks
    * unexpected directories
* no-changes-needed is a success case (idempotency exits 0)


### yelp1

* --update now works more generally and reliably (e.g. virtualenv --python=python2.7)


## virtualenv-tools

This repository contains scripts we're using at Fireteam for our
deployment of Python code.  We're using them in combination with
salt to build code on one server on a self contained virtualenv
and then move that over to the destination servers to run.

### Why not virtualenv --relocatable?

For starters: because it does not work.  relocatable is very
limited in what it does and it works at runtime instead of
making the whole thing actually move to the new location.  We
ran into a ton of issues with it and it is currently in the
process of being phased out.

### Why would I want to use it?

The main reason you want to use this is for build caching.  You
have one folder where one virtualenv exists, you install the
latest version of your codebase and all extensions in there, then
you can make the virtualenv relocate to a target location, put it
into a tarball, distribute it to all servers and done!

### Example flow:

First time: create the build cache

```
$ mkdir /tmp/build-cache
$ virtualenv --distribute /tmp/build-cache
```

Now every time you build:

```
$ . /tmp/build-cache/bin/activate
$ pip install YourApplication
```

Build done, package up and copy to whatever location you want to have it.

Once unpacked on the target server, use the virtualenv tools to
update the paths and make the virtualenv magically work in the new
location.  For instance we deploy things to a path with the
hash of the commit in:

```
$ virtualenv-tools --update-path /srv/your-application/<hash>
```

Compile once, deploy whereever.  Virtualenvs are completely self
contained.  In order to switch the current version all you need to
do is to relink the builds.
