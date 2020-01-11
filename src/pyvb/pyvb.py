# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Jared Crapo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
"""
Entry point for 'pyvb' command line program
"""

import subprocess
import re


def _get_pythons():
    """Get a list of pythons that are available to us"""
    process = subprocess.run(
        ['pyenv', 'install', '--list'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
        )
    pythons = process.stdout.split('\n')
    return pythons


def find_latest_version(major_minor):
    """Given a major.minor specifier, find the latest available python version to pyenv

    >>> print(find_latest_version("3.4"))
    3.4.10
    """
    pythons = _get_pythons()
    # strip spaces
    pythons = list(map(lambda x: x.strip(), pythons))

    # ignore dev, beta and rc versions
    prereleases = re.compile(r'(dev$|rc[0-9]+$|b[0-9]+$)')
    pythons = list(filter(lambda x: not prereleases.search(x), pythons))

    # iterate the list backwards (we want the highest version, which appears
    # later in the `pyenv` output) to find the highest matching version
    latest = None
    for version in reversed(pythons):
        if version.startswith(major_minor):
            latest = version
            break
    return latest
