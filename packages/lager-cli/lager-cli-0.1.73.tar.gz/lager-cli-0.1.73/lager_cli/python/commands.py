"""
    lager.python.commands

    Commands for running lager python
"""
import os
import sys
import threading
import itertools
import functools
import signal
import click
import trio
from ..gdbserver.tunnel import serve_tunnel
from ..context import get_default_gateway
from ..util import (
    stream_python_output, zip_dir, SizeLimitExceeded,
    FAILED_TO_RETRIEVE_EXIT_CODE,
    SIGTERM_EXIT_CODE,
    SIGKILL_EXIT_CODE,
    StreamDatatypes,
    stdout_is_stderr,
)
from ..paramtypes import EnvVarType
from ..exceptions import OutputFormatNotSupported

MAX_ZIP_SIZE = 10_000_000  # Max size of zipped folder in bytes

_ORIGINAL_SIGINT_HANDLER = signal.getsignal(signal.SIGINT)

def sigint_handler(kill_python, _sig, _frame):
    """
        Handle Ctrl+C by restoring the old signal handler (so that subsequent Ctrl+C will actually
        stop python), and send the SIGTERM to the running docker container.
    """
    click.echo(' Attempting to stop Lager Python job')
    signal.signal(signal.SIGINT, _ORIGINAL_SIGINT_HANDLER)
    kill_python(signal.SIGINT)

def _do_exit(exit_code):
    if exit_code == FAILED_TO_RETRIEVE_EXIT_CODE:
        click.secho('Failed to retrieve script exit code.', fg='red', err=True)
    elif exit_code == SIGTERM_EXIT_CODE:
        click.secho('Gateway script terminated due to timeout.', fg='red', err=True)
    elif exit_code == SIGKILL_EXIT_CODE:
        click.secho('Gateway script forcibly killed due to timeout.', fg='red', err=True)
    sys.exit(exit_code)

def debug_tunnel(ctx, gateway):
    host = 'localhost'
    port = 5555
    connection_params = ctx.obj.websocket_connection_params(socktype='pdb', gateway_id=gateway)
    try:
        trio.run(serve_tunnel, host, port, connection_params, None)
    except PermissionError as exc:
        click.secho(str(exc), fg='red', err=True)
        if ctx.obj.debug:
            raise
    except OSError as exc:
        click.secho(f'Could not start remote pdb on port {port}: {exc}', fg='red', err=True)
        if ctx.obj.debug:
            raise

_SIGNAL_MAP = {
    'SIGINT': 2,
    'SIGQUIT': 3,
    'SIGABRT': 6,
    'SIGKILL': 9,
    'SIGUSR1': 10,
    'SIGUSR2': 12,
    'SIGTERM': 15,
    'SIGSTOP': 19,
}

_SIGNAL_CHOICES = click.Choice(list(_SIGNAL_MAP.keys()), case_sensitive=False)

def _get_signal_number(name):
    return _SIGNAL_MAP[name.upper()]

@click.command()
@click.pass_context
@click.argument('runnable', required=False, type=click.Path(exists=True))
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected')
@click.option('--image', default='lagerdata/gatewaypy3:v0.1.68', help='Docker image to use for running script')
@click.option(
    '--env',
    multiple=True, type=EnvVarType(), help='Environment variables to set for the python script. '
    'Format is `--env FOO=BAR` - this will set an environment varialbe named `FOO` to the value `BAR`')
@click.option(
    '--passenv',
    multiple=True, help='Environment variables to inherit from the current environment and pass to the python script. '
    'This option is useful for secrets, tokens, passwords, or any other values that you do not want to appear on the '
    'command line. Example: `--passenv FOO` will set an environment variable named `FOO` in the python script to the value'
    'of `FOO` in the current environment.')
@click.option('--kill', is_flag=True, default=False, help='Terminate a running python script')
@click.option('--signal', 'signum', default='SIGTERM', type=_SIGNAL_CHOICES, help='Signal to use with --kill', show_default=True)
@click.option('--timeout', type=click.INT, required=False, help='Max runtime in seconds for the python script')
@click.option('--detach', '-d', is_flag=True, required=False, default=False, help='Detach')
@click.argument('args', nargs=-1)
def python(ctx, runnable, gateway, image, env, passenv, kill, signum, timeout, detach, args):
    """
        Run a python script on the gateway
    """
    if not runnable and not kill:
        raise click.UsageError('Please supply a RUNNABLE or the --kill option')

    session = ctx.obj.session
    if gateway is None:
        gateway = get_default_gateway(ctx)

    if kill:
        signum = _get_signal_number(signum)
        resp = session.kill_python(gateway, signum)
        resp.raise_for_status()
        return

    thread = threading.Thread(target=debug_tunnel, args=(ctx, gateway), daemon=True)
    thread.start()

    post_data = [
        ('image', image),
        ('stdout_is_stderr', stdout_is_stderr()),
        ('detach', '1' if detach else '0'),
    ]
    post_data.extend(
        zip(itertools.repeat('args'), args)
    )
    post_data.extend(
        zip(itertools.repeat('env'), env)
    )
    post_data.extend(
        zip(itertools.repeat('env'), [f'{name}={os.environ[name]}' for name in passenv])
    )

    if timeout is not None:
        post_data.append(('timeout', timeout))

    if os.path.isfile(runnable):
        post_data.append(('script', open(runnable, 'rb')))
    elif os.path.isdir(runnable):
        try:
            max_content_size = 20_000_000
            zipped_folder = zip_dir(runnable, max_content_size=max_content_size)
        except SizeLimitExceeded:
            click.secho(f'Folder content exceeds max size of {max_content_size:,} bytes', err=True, fg='red')
            ctx.exit(1)

        if len(zipped_folder) > MAX_ZIP_SIZE:
            click.secho(f'Zipped module content exceeds max size of {MAX_ZIP_SIZE:,} bytes', err=True, fg='red')
            ctx.exit(1)

        post_data.append(('module', zipped_folder))

    resp = session.run_python(gateway, files=post_data)
    kill_python = functools.partial(session.kill_python, gateway)
    handler = functools.partial(sigint_handler, kill_python)
    signal.signal(signal.SIGINT, handler)

    try:
        for (datatype, content) in stream_python_output(resp):
            if datatype == StreamDatatypes.EXIT:
                _do_exit(content)
            elif datatype == StreamDatatypes.STDOUT:
                click.echo(content, nl=False)
            elif datatype == StreamDatatypes.STDERR:
                click.echo(content, nl=False, err=True)
            elif datatype == StreamDatatypes.OUTPUT:
                click.echo(content)

    except OutputFormatNotSupported:
        click.secho('Response format not supported. Please upgrade lager-cli', fg='red', err=True)
        sys.exit(1)
