# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import os
import sys
import logging
import click

# add mldock package to path
sys.path.insert(1, ".")

from mldock.__version__ import __version__
from mldock.__init__ import MLDOCK_LOGO
# from mldock.command.initialize import init
from mldock.command.container import container
from mldock.command.local import local
from mldock.command.cloud import cloud
from mldock.log import configure_logger

click.disable_unicode_literals_warning = True

CLI_VERSION = 'Version: cli {}'.format(__version__)

@click.group()
@click.version_option(message='{}\n{}'.format(MLDOCK_LOGO, CLI_VERSION))
@click.option(u"-v", u"--verbose", count=True, help=u"Turn on debug logging")
@click.pass_context
def cli(ctx, verbose):
    """
    CLI tool built to add simple functionality to sagify development.
    """
    _FILE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    logger=configure_logger('mldock', verbose=verbose)
    logger.info(MLDOCK_LOGO)
    logger.info(CLI_VERSION)
    ctx.obj = {'verbose': verbose, 'helper_library_path':_FILE_DIR_PATH, 'logo':MLDOCK_LOGO}

def add_commands(cli):

    cli.add_command(container)
    cli.add_command(local)
    cli.add_command(cloud)

add_commands(cli)

if __name__ == '__main__':
    cli()
