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

import argparse
import subprocess
import re

import pyvb

# pylint: disable=too-few-public-methods
class Environment():
    """Data class to hold info about a particular python environment"""
    majmin_re = re.compile(r'\d+\.\d+')

    def __init__(self, name=None, version=None):
        self.name = name
        self.version = version

    @property
    def major_minor(self):
        """return a string of the major and minor components of the version"""
        if self.version:
            match = re.match(self.majmin_re, self.version)
            if match:
                return match.group(0)
        return None


class Pyvb():
    """pyvb command line program class"""

    def __init__(self):
        """initialize"""
        self.dryrun = False
        self.verbose = False

    @classmethod
    def _build_parser(cls):
        """Build the argument parser"""
        parser = argparse.ArgumentParser(
            description='Create pyenv and virtualenv python environments',
        )

        basename_help = 'the base environment name'
        parser.add_argument('basename', help=basename_help)

        # write_help = 'write created environment names to .python-version in the current directory'
        # parser.add_argument('-w', '--write', action='store_true', help=write_help)

        # append_help = 'created environment names to .python-version in the current directory'
        # parser.add_argument('-a', '--append', action='store_true', help=append_help)

        dryrun_help = "Don't execute anything, but show what would be done. Implies -v."
        parser.add_argument('--dry-run', '-n',
                            action='store_true',
                            default=False,
                            help=dryrun_help
                            )

        verbose_help = 'Display progress information about progress'
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            default=False,
                            help=verbose_help
                            )

        version_help = 'show the version of pyvb and exit'
        parser.add_argument('--version',
                            action='version',
                            version=pyvb.__version__,
                            help=version_help
                            )

        return parser

    def status_message(self, msg):
        """display a status message"""
        if self.verbose:
            print('pyvb: {}'.format(msg))

    def main(self, argv=None):
        """Entry point for 'pyvb' command line program

        :return: an exit code

        0 = command completed successfully
        1 = pyenv, a required dependency, is not installed
        """
        parser = self._build_parser()
        args = parser.parse_args(argv)

        self.dryrun = args.dry_run
        self.verbose = args.verbose
        if self.dryrun:
            self.verbose = True

        if not self.have_pyenv():
            msg = '{0}: {0} requires pyenv, which is not installed'.format(parser.prog)
            print(msg)
            return 1

        # build a list of environments
        pythons = self.get_pythons()
        environments = []
        for majmin in self.minor_pythons():
            env = Environment()
            env.name = '{}-{}'.format(args.basename, majmin)
            env.version = self.find_latest_version(pythons, majmin)
            environments.append(env)

        # create each environment
        try:
            for env in environments:
                self.create_environment(env)
        except subprocess.CalledProcessError:
            return 1

        return 0

    def get_pythons(self):
        """Use pyenv to get a list of pythons that are available to us"""
        self.status_message('retrieving available pythons from pyenv')

        process = subprocess.run(
            ['pyenv', 'install', '--list'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            )
        pythons = process.stdout.split('\n')
        return pythons

    def have_pyenv(self):
        """Check if pyenv is installed"""
        self.status_message('checking if pyenv is installed')
        process = subprocess.run(
            ['pyenv', '--version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        return process.returncode == 0

    @classmethod
    def minor_pythons(cls):
        """Return a list of standard python major.minor versions

        Standard python versions are those that are not deprecated.
        """
        return ["3.8", "3.7", "3.6", "3.5"]

    @classmethod
    def find_latest_version(cls, pythons, major_minor):
        """Given a major.minor specifier, find the latest available python version to pyenv

        >>> pythons = getfixture('pythons')
        >>> prog = Pyvb()
        >>> print(prog.find_latest_version(pythons, '3.4'))
        3.4.10

        :return: a version string like 3.8.1 or None if there are no matches
        """
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

    def create_environment(self, env):
        """Create an environment specified by the passed instance of an Environment class"""
        self.install_python(env.version)
        self.status_message('deleting environment {}'.format(env.name))
        if not self.dryrun:
            subprocess.run(['pyenv', 'uninstall', '-f', env.name], check=False)

        self.status_message('creating environment {} with version {}'.format(env.name, env.version))
        if not self.dryrun:
            argv = ['pyenv', 'virtualenv', '-p']
            argv.append('python{}'.format(env.major_minor))
            argv.append(env.version)
            argv.append(env.name)
            subprocess.run(argv, check=True)

    def install_python(self, version):
        """Use pyenv to install a python version, ie major.minor.version, ie 3.8.1

        :version: a version string like 3.8.1

        Throws a CalledProcessError exception if an error occurs
        """
        self.status_message('running pyenv to install python {}'.format(version))
        if not self.dryrun:
            subprocess.run(
                ['pyenv', 'install', '-s', version],
                check=True,
            )
