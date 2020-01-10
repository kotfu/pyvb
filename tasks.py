#
# -*- coding: utf-8 -*-
"""Development related tasks to be run with 'invoke'"""

import invoke

# create namespaces
namespace = invoke.Collection()


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
