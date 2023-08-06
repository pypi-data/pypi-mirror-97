"""
General commands


"""
import os
import click
import json

from scintillant import addons_versions


def show_testsuite_version():
    if not os.path.exists(os.getcwd() + '/.snlt'): return
    snlt = json.load(open(os.getcwd() + '/.snlt'))
    if 'testsuite' not in snlt: return
    testsuite = snlt['testsuite']
    if 'version' not in testsuite:
        click.echo("The testsuite version is undefined. "
                   "Try reinstalling with 'snlt testsuite --reinstall'.")
    elif not (addons_versions['__testsuite__'] == testsuite['version']):
        click.echo("The version of 'testsuite' installed in your environment "
                   "is outdated. To get the new version use the 'snlt "
                   "testsuite --upgrade' command")
    else:
        click.echo(f"testsuite {testsuite['version']}")
