[![](https://badgen.net/pypi/v/yappyg)](https://pypi.org/project/yappyg/)
[![](https://badgen.net/pypi/license/yappyg)](https://pypi.org/project/yappyg/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/yappyg)
![PyPI - Status](https://img.shields.io/pypi/status/yappyg.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

yappyG
======

yappyG is another package for pythonable Git

This a quick and dirty fork of briGit:
Very simple git wrapper module licensed under BSD
Copyright (C) 2011 by Florian Mounier, Kozea


Installation
------------

Use pip :

    pip install yappyg

How it works
------------

This is a very gentle wrapping of command-line git, allowing mostly free-flowing passing of git commands from python. This was mostly born from issues in using the (fantastic) briGit package in Jupyter Notebooks. Because briGit uses `Popen` to call git, we lose the ability to respond to Username/Password prompts when not using a strictly command-line interface. Instead we use `pexpect`, and set up a few patterns to wait on. Off the top of my head I could only think of *Username:* and *Password:*, other promprts will end up hanging to `expect` line until it times out. Additional patterns should be added to expectations to fix that.

Usage
-----

```python
from yappyg import Git
new_repo = Git("~/brigit/new_repo")  # Will do a git init
git = Git("~/brigit/i_forked_this_from_brigit",
    "git://github.com/lucasdurand/yappyg.git",
     quiet=False)  # Will do a git clone

# Git commands passed through as methods
git.pull()

import os
open(os.path.expanduser("~/brigit/i_forked_this_from_brigit/myNewFile"), "a+").close()
git.add("myNewFile")
# Use *args and **kwargs to pass commands
git.commit("-a", message="Adding myNewFile") # git commit -a --message=
# There's also some utils command:
git.pretty_log()
git.push() # if you have push rights
```
