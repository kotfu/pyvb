#
# -*- coding: utf-8 -*-
"""Development related tasks to be run with 'invoke'"""

import os
import shutil

import invoke

# shared function
def rmrf(items, verbose=True):
    "Silently remove a list of directories or files"
    if isinstance(items, str):
        items = [items]

    for item in items:
        if verbose:
            print("Removing {}".format(item))
        shutil.rmtree(item, ignore_errors=True)
        # rmtree doesn't remove bare files
        try:
            os.remove(item)
        except FileNotFoundError:
            pass

# create namespaces
namespace = invoke.Collection()
namespace_clean = invoke.Collection('clean')
namespace.add_collection(namespace_clean, 'clean')

#####
#
# pytest, tox, pylint, and codecov
#
#####
@invoke.task
def pytest(context):
    "Run tests and code coverage using pytest"
    context.run("pytest --cov=pyvb")
namespace.add_task(pytest)

@invoke.task
def pytest_clean(context):
    "Remove pytest cache and code coverage files and directories"
    #pylint: disable=unused-argument
    dirs = ['.pytest_cache', '.cache', '.coverage']
    rmrf(dirs)
namespace_clean.add_task(pytest_clean, 'pytest')

@invoke.task
def pylint(context):
    "Check code quality using pylint"
    context.run('pylint --rcfile=src/pyvb/pylintrc src/pyvb')
namespace.add_task(pylint)

# flake8 - linter and tool for style guide enforcement and linting
@invoke.task
def flake8(context):
    "Run flake8 linter and tool for style guide enforcement"
    context.run("flake8 src/pyvb")
namespace.add_task(flake8)

#
# make a dummy clean task which runs all the tasks in the clean namespace
clean_tasks = list(namespace_clean.tasks.values())
@invoke.task(pre=list(namespace_clean.tasks.values()), default=True)
def clean_all(context):
    "Run all clean tasks"
    #pylint: disable=unused-argument
    pass
namespace_clean.add_task(clean_all, 'all')
