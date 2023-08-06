import click
import PyInquirer as inq
from examples import custom_style_1

from wave_cli.services.backend_services import Backend


@click.command(name='delete', help='Delete devices. Use options to filter devices')
@click.pass_context
@click.option('-sn', '--serial-number', help='Device serial number')
@click.option('-id', '--device-id', help='Device id', default=None)
def delete(ctx, serial_number, device_id):
    if not serial_number and not device_id:
        serial_number = inq.prompt(
                questions=[{'type': 'input', 'name': 'serial_number', 'message': 'Enter serial_number'}],
                style=custom_style_1
            )['serial_number']
    backend = Backend(ctx)
    where = {
      "deviceId": device_id,
      "serialNumber": serial_number,
    }
    dev = backend.get_devices_list(where)
    if len(dev) == 0:
        click.secho('  DEVICE NOT FOUND!', fg='yellow')
        exit(1)
    confirm = inq.prompt(
        questions=[{
            'type': 'confirm',
            'name': 'confirm',
            'default': False,
            'message': 'Are you sure to delete the device "{0}" ?'.format(dev[0]['store'])
        }],
        style=custom_style_1
    )['confirm']
    if confirm:
        backend.delete_device(device_id=dev[0]['deviceId'])
