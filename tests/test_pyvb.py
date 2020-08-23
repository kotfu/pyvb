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

def test_find_latest_version(pythons):
    #pyfunc = mocker.patch("pyvb.pyvb.get_pythons")
    #pyfunc.return_value = pythons
    prog = pyvb.Pyvb()
    assert prog.find_latest_version(pythons, '3.8') == '3.8.1'
    assert prog.find_latest_version(pythons, '1.4') is None
    assert prog.find_latest_version(pythons, 'fred') is None
    assert prog.find_latest_version(pythons, '3.9') is None
    assert prog.find_latest_version(pythons, '3.6') == '3.6.10'

def test_environment():
    env = pyvb.pyvb.Environment('fred', '3.8.1')
    assert env.major_minor == '3.8'
