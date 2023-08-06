import click
import re
import PyInquirer as inq
from examples import custom_style_1

from wave_cli.services.validate_services import StringValidate
from wave_cli import COMMAND_NAME
from wave_cli.services.backend_services import Backend


@click.command(name='update', help='Update devices. Use options to filter devices')
@click.pass_context
@click.argument('args', nargs=1, default=None, required=False)
@click.option('-v', '--firmware-version', help='Firmware version', is_eager=True)
@click.option('-sn', '--serial-number', help='Device serial number', default=None, is_eager=True)
@click.option('-pn', '--part-number', help='Device part number', default=None, is_eager=True)
@click.option('-id', '--device-id', help='Device id', default=None, is_eager=True)
@click.option('-n', '--device-name', help='Device name', default=None, is_eager=True)
@click.option('-c', '--company', help='Company name', default=None, is_eager=True)
@click.option('-st', '--store', help='Store name', default=None, is_eager=True)
@click.option('-stn', '--store-number', help='Store number', default=None, is_eager=True)
@click.option('-cl', '--cluster', help='Cluster name', default=None, is_eager=True)
@click.option('-w', '--when', help='Update start time', default=None, is_eager=True)
def update(ctx, args, firmware_version, serial_number, part_number, device_id, device_name, company, store, store_number, cluster, when):
    try:
        if args == 'force':
            force_update = True
        else:
            force_update = False
        answer = inq.prompt(
            style=custom_style_1,
            questions=[
                {
                    'type': 'input',
                    'name': 'desired_version',
                    'message': 'Enter firmware version to update',
                    'validate': StringValidate,
                }
            ]
        )
        desired_version = answer['desired_version']
        if not firmware_version and \
                not serial_number and \
                not device_id and \
                not device_name and \
                not company and \
                not store and \
                not store_number and \
                not cluster:
            confirm = inq.prompt(
                style=custom_style_1,
                questions=[{
                    'type': 'confirm',
                    'name': 'confirm',
                    'default': False,
                    'message': 'Are you trying update all devices?'
                }],
            )['confirm']
            if not confirm:
                click.secho(message='\nBye!')
                exit(1)
            answer = inq.prompt(
                style=custom_style_1,
                questions=[
                    {
                        'type': 'input',
                        'name': 're_desired_version',
                        'message': 'So to confirm, type firmware version again [{0}]'.format(desired_version),
                        'validate': StringValidate,
                    }
                ]
            )
            re_desired_version = answer['re_desired_version']
            if desired_version != re_desired_version:
                click.secho('Not matched!', fg='red')
                exit(1)
        backend = Backend(ctx)
        where = {
            "firmwareVersion": firmware_version,
            "deviceId": device_id,
            "store": store,
            "storeNumber": store_number,
            "cluster": cluster,
            "company": company,
            "serialNumber": serial_number,
            "deviceName": device_name,
            "partNumber": part_number
        }
        result = backend.update_devices(desired_version=desired_version, where=where, is_forced=force_update, when=when)
        click.secho("")
        for key in result:
            row_length = 25
            splitted_key = re.findall('.[^A-Z]*', key)
            cap_splitted_key = [k.capitalize() for k in splitted_key]
            joined = ' '.join(cap_splitted_key)
            txt = "  {0}:".format(joined) + ' ' * (row_length - len(joined)) + "{0}".format(result[key])
            click.secho(txt, bold=True, fg='blue')
        click.secho()
        click.secho("Run `{0} show device` to tracking update states.".format(COMMAND_NAME))
        click.secho()
    except Exception as e:
        exit()
