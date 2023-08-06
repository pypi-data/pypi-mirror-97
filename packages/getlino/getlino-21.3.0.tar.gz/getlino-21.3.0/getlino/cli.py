# Copyright 2019-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""The main entry point for the :command:`getlino` command.
"""

import click
import distro

from .setup_info import SETUP_INFO

from .configure import configure
from .startsite import startsite

@click.group(help="""
A command-line tool for installing Lino in different environments.
See http://getlino.lino-framework.org for more information.

This is getlino version {} running on {}.
""".format(SETUP_INFO['version'], distro.name(pretty=True)))
def main():
    pass

main.add_command(configure)
main.add_command(startsite)

if __name__ == '__main__':
    main()
    # main(auto_envvar_prefix='GETLINO')
