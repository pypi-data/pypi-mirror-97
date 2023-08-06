import logging

from cliff.command import Command
from enough import settings
from enough.common.openstack import OpenStack
from enough.common import dotenough
from enough.common import options


class Create(Command):
    "Create backups."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('volumes', nargs='*')
        options.set_options(parser)
        return parser

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        d = dotenough.DotEnoughOpenStack(settings.CONFIG_DIR, args['domain'])
        d.ensure()
        o = OpenStack(settings.CONFIG_DIR, **args)
        o.backup_create(args['volumes'])


class Prune(Command):
    "Prune old backup volumes and their snapshots."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('days', type=int, default=30)
        options.set_options(parser)
        return parser

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        d = dotenough.DotEnoughOpenStack(settings.CONFIG_DIR, args['domain'])
        d.ensure()
        o = OpenStack(settings.CONFIG_DIR, **args)
        o.backup_prune(args['days'])
        o.volume_prune(args['days'])
