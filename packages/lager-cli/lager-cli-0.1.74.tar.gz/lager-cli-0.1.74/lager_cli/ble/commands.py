"""
    lager.ble.commands

    Commands for BLE
"""
import math
import click
from ..context import get_default_gateway
from ..paramtypes import CanFrameType, CanFilterType, CanbusRange
from ..status import run_job_output

@click.group(name='ble')
def ble():
    """
        Lager BLE commands
    """
    pass

@ble.command('scan')
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected')
def scan(ctx, gateway):
    """
        Scan for BLE devices
    """
    if gateway is None:
        gateway = get_default_gateway(ctx)

    session = ctx.obj.session
    resp = session.ble_scan(gateway)
    print(resp.json())
