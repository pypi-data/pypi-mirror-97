import argparse
import code
import readline
import rlcompleter  # noqa  provides python shell autocomplete
import dli
import signal
import sys

from distutils.util import strtobool
from dli import connect

try:
    import IPython  # noqa
    from traitlets.config.loader import Config  # noqa
except ImportError:
    IPython = None
    Config = None


def aws(dli_client):
    try:
        dli_client.aws_authenticator.start()
        dli_client.aws_authenticator.join()
    except (KeyboardInterrupt, SystemExit):
        print('\n')
        dli_client.logger.info('Exiting')
    except Exception:
        sys.exit(1)


def shell(dli_client, basic_shell=False):
    banner = (
        f'DLI {dli.__version__} session started. '
        'Can be used by accessing `client`\n'
    )

    if IPython and not basic_shell:
        config = Config()
        config.TerminalInteractiveShell.banner2 = banner
        IPython.start_ipython(
            argv=[], user_ns={'client': dli_client},
            config=config
        )
    else:
        readline.parse_and_bind('tab:complete')
        console = code.InteractiveConsole(locals={
            'client': dli_client
        })
        console.interact(
            banner=banner
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--root_url', default=None,
        type=str,
    )

    parser.add_argument(
        '--host', default=None,
        type=str,
    )

    parser.add_argument(
        '--debug', default=None,
        type=strtobool,
    )

    parser.add_argument(
        '--strict', default=None,
        type=strtobool,
    )

    parser.add_argument(
        '--use_keyring', default=None,
        type=strtobool,
    )

    parser.add_argument(
        '--log_level', default=None,
        type=str,
    )

    subparser = parser.add_subparsers(dest='subcommand')
    subparser.add_parser(
        'aws',
        help=(
            'Runs a process which writes to ~/.aws/credentials. Keeping it '
            'synced with the credentials provided by the DLI.'
        )
    )

    shell_parser = subparser.add_parser(
        'shell',
        help=(
            'Runs the DLI in a Python shell. (IPython if available).'
        )
    )

    shell_parser.add_argument(
        '--basic', action='store_true',
        help='Use basic Python shell without IPython',
        default=False
    )

    subparser.add_parser(
        'version',
        help=(
            'Displays the version'
        )
    )

    subparser.required = True
    args = parser.parse_args()

    connection_args = {
        k:v for k,v in vars(args).items() if v is not None
    }

    basic_shell = connection_args.pop('basic', False)
    subcommand = connection_args.pop('subcommand')

    dli_client = connect(**connection_args)

    if subcommand == 'aws':
        aws(dli_client)

    if subcommand == 'shell':
        shell(dli_client, basic_shell)

    if subcommand == 'version':
        print(f'{dli.__version__}')

    sys.exit(0)
