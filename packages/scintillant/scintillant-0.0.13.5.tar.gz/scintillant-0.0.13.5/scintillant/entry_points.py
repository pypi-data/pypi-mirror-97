"""
scintillant.entry_points.py
~~~~~~~~~~~~~~~~~~~~~~

This module contains the entry-point functions for the scintillant module,
that are referenced in setup.py.
"""
from scintillant import about
from scintillant.commands.templates import start_bottle_skill
from scintillant.commands.testsuite import start_test_suite
from scintillant.commands.utils import show_testsuite_version

import click


@click.group()
def main() -> None:
    """Main package entry point.

    Delegates to other functions based on user input.
    """
    pass


@main.command()
@click.option('--name', default='bottle-skill-template',
              help="Name of the skill being developed")
def bottle(name):
    """Download the latest skill template"""
    start_bottle_skill(skill_name=name)


@main.command()
def version():
    """Show version of framework"""
    click.echo('Scintillant Framework ' + about['__version__'])
    show_testsuite_version()


@main.command()
def testsuite():
    """Downloads and runs a test environment for the skill."""
    start_test_suite()