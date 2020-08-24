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
pyvb test suite
"""

import pyvb


def test_find_latest_version(prog):
    assert prog.find_latest_version("3.8") == "3.8.1"
    assert prog.find_latest_version("1.4") is None
    assert prog.find_latest_version("fred") is None
    assert prog.find_latest_version("3.9") is None
    assert prog.find_latest_version("3.6") == "3.6.10"


def test_environment():
    env = pyvb.pyvb.Environment("fred", "3.8.1")
    assert env.major_minor == "3.8"


def test_select_pythons_commas(prog):
    assert prog.select_pythons(["3.7.1, 3.8.1"]) == ["3.7.1", "3.8.1"]
    assert prog.select_pythons(["3.6.0,3.7.1,3.8.0"]) == ["3.6.0", "3.7.1", "3.8.0"]
    assert prog.select_pythons(["3.6", "3.7,3.8"]) == ["3.6.10", "3.7.6", "3.8.1"]


def test_select_pythons_exact(prog):
    assert prog.select_pythons(["3.8.1"]) == ["3.8.1"]


def test_all_pythons(prog, pythons):
    all_pythons = prog.all_pythons()
    assert len(all_pythons) == len(pythons.split("\n")) - 1
