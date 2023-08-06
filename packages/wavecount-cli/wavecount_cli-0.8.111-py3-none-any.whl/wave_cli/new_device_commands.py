import pydash as _
import click
import PyInquirer as inq
from examples import custom_style_1
from pydash.collections import find

from wave_cli.utils import save_config
from wave_cli.services.backend_services import Backend
from wave_cli.services.validate_services import IntValidate, PartNumberValidate, StringValidate, SerialNumberValidate


@click.command(name='new', help='Register a new device.')
@click.pass_context
def new(ctx):
    try:
        roles: str = ctx.obj['roles']
        backend_service = Backend(context=ctx)
        result = backend_service.sync_cache()
        companies = result['companies']
        company_choices = ['new', *_.map_(companies, 'company')]
        part_numbers = result['partNumbers']
        part_numbers_choices = []
        if roles == 'admin':
            part_numbers_choices.extend(['new'])
        part_numbers_choices.extend(part_numbers)
        answer = inq.prompt(
            questions=[
                {
                    'type': 'input',
                    'name': 'serial_number',
                    'message': 'Enter device "serial number"',
                    'validate': SerialNumberValidate,
                },
                {
                    'type': 'list',
                    'name': 'part_number',
                    'message': 'Select "part number"',
                    'choices': part_numbers_choices,
                    'validate': PartNumberValidate,
                }
            ],
            style=custom_style_1
        )
        serial_number: str = answer['serial_number']
        part_number: str = answer['part_number']
        if part_number == 'new':
            answer = inq.prompt(
                style=custom_style_1,
                questions=[
                    {
                        'type': 'input',
                        'name': 'part_number',
                        'message': 'Enter device "part number"',
                        'validate': PartNumberValidate,
                    }
                ],
            )
            part_number: str = answer['part_number']
        answer = inq.prompt(
            questions=[
                {
                    'type': 'list',
                    'name': 'company',
                    'message': 'Select "company"',
                    'choices': company_choices,
                    'validate': StringValidate,
                }
            ],
            style=custom_style_1
        )
        company: str = answer['company']
        if company == 'new':
            answers = inq.prompt(
                style=custom_style_1,
                questions=[
                    {
                        'type': 'input',
                        'name': 'company',
                        'message': 'Enter "company"',
                        'validate': StringValidate,
                    },
                    {
                        'type': 'input',
                        'name': 'store',
                        'message': 'Enter "store"',
                        'validate': StringValidate,
                    },
                    {
                        'type': 'input',
                        'name': 'store_number',
                        'message': 'Enter "store number"',
                        'validate': IntValidate,
                    },
                ],
            )
            company: str = answers['company']
            store: str = answers['store']
            store_number: str = answers['store_number']
        else:
            store_choices = ['new']
            company_item = _.find(companies, {'company': company})
            stores_items = company_item['stores']
            stores = _.uniq(_.map_(stores_items, 'store'))
            store_choices.extend(stores)
            answer = inq.prompt(
                style=custom_style_1,
                questions=[
                    {
                        'type': 'list',
                        'name': 'store',
                        'message': 'Enter "store"',
                        'choices': store_choices,
                        'validate': StringValidate,
                    },
                ],
            )
            store: str = answer['store']
            if store == 'new':
                answer = inq.prompt(
                    style=custom_style_1,
                    questions=[
                        {
                            'type': 'input',
                            'name': 'store',
                            'message': 'Enter "store"',
                            'validate': StringValidate,
                        },
                        {
                            'type': 'input',
                            'name': 'store_number',
                            'message': 'Enter "store number"',
                            'validate': IntValidate,
                        },
                    ],
                )
                store: str = answer['store']
                store_number: str = answer['store_number']
            else:
                store_item = _.find(stores_items, {'store': store})
                store_number: str = store_item['storeNumber']
        data = {
            'store': store,
            'company': company,
            'storeNumber': store_number,
            'serialNumber': serial_number,
            'partNumber': part_number,
        }
        device = backend_service.register_device(data)
        dev_id = device['deviceId']
        prim_key = device['symmetricKey']['primaryKey']
        comp = device['company']
        store = device['store']
        store_num = device['storeNumber']
        sn = device['serialNumber']
        pn = device['partNumber']
        click.secho(' Part Number:    {}'.format(pn), fg='green')
        click.secho(' Serial Number:  {}'.format(sn), fg='green')
        click.secho(' Device Id:      {}'.format(dev_id), fg='green')
        click.secho(' Primary Key:    {}'.format(prim_key), fg='green')
        click.secho(' Company:        {}'.format(comp), fg='green')
        click.secho(' Store:          {}'.format(store), fg='green')
        click.secho(' Store Number:   {}'.format(store_num), fg='green')
        click.secho()
    except Exception as e:
        exit(1)
