from argparse import Action, Namespace

from cvm.commands.command import Command
from cvm.services.composer_service import ComposerService
from cvm.services.github_service import GitHubService


class InitCommand(Command):
    NAME = 'init'
    DESCRIPTION = 'Initialize the folder to use the cvm .cvmconfig file'

    def exec(self, args: Namespace):
        desired_version = args.version[0]

        github_service = GitHubService('composer', 'composer')
        composer_service = ComposerService(github_service)

    @staticmethod
    def define_signature(parser: Action):
        install_parser = parser.add_parser(InstallCommand.NAME, help=InstallCommand.DESCRIPTION)
        install_parser.add_argument(
            'version',
            nargs=1,
            help='Composer version to install.',
            metavar='{version}'
        )
