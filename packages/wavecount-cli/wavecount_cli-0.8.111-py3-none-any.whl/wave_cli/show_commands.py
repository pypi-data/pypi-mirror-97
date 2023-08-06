import click
import datetime
import pydash as _

from wave_cli.services.backend_services import Backend


@click.group(name='show', add_help_option=False, short_help='Subcommands: [device, error]', help='Show commands managements')
def show():
    pass


@click.command(name='error', help='Show avtive errors.')
@click.pass_context
def error(ctx):
    backend_service = Backend(ctx)
    ef_list = backend_service.get_error_flags()
    if len(ef_list):
        row_len = 114
        block_len = round(row_len / 6)
        sep = '│'
        t_com = ' Company'
        t_sto = ' Store'
        t_dNm = ' Device'
        t_srl = ' S/N'
        t_err = ' Error'
        tz = str(datetime.datetime.utcnow().astimezone().tzinfo).split(' ')[0]
        t_dte = ' Date   [{0}]'.format(tz)
        click.secho('╭' + '─' * (row_len - 6) + '╮')
        click.secho(sep + t_com + ' ' * (block_len - len(t_com) - 4) +
                    sep + t_sto + ' ' * (block_len - len(t_sto) - 4) +
                    sep + t_dNm + ' ' * (block_len - len(t_dNm) - 4) +
                    sep + t_srl + ' ' * (block_len - len(t_srl) - 4) +
                    sep + t_err + ' ' * (block_len - len(t_err) + 6) +
                    sep + t_dte + ' ' * (block_len - len(t_dte) - 1) +
                    sep)
        click.secho('╞' + '═' * (row_len - 6) + '╡')
        prev_dId = ' '
        for ef in ef_list:
            for f in ef['errorFlags']:
                if len(ef['deviceName']) < len(t_dNm + ' ' * (block_len - len(t_dNm) - 4)):
                    dNm = ' {0}'.format(ef['deviceName'])
                else:
                    dNm = ' {0}..'.format(ef['deviceName'][0:(len(t_dNm + ' ' * (block_len - len(t_dNm) - 4)) - 7)])
                if len(ef['company']) < len(t_com) + (block_len - len(t_com) - 4):
                    com = ' {0}'.format(ef['company'])
                else:
                    com = ' {0}..'.format(ef['company'][0:(len(t_com + ' ' * (block_len - len(t_com) - 4)) - 7)])
                if len(ef['store']) < len(t_sto) + (block_len - len(t_sto) - 4):
                    sto = ' {0}'.format(ef['store'])
                else:
                    sto = ' {0}..'.format(ef['store'][0:(len(t_sto + ' ' * (block_len - len(t_sto))) - 7)])
                if len(ef['serialNumber']) < len(t_srl + ' ' * (block_len - len(t_srl))):
                    srl = ' {0}'.format(ef['serialNumber'])
                else:
                    srl = ' {0}..'.format(ef['serialNumber'][0:(len(t_srl + ' ' * (block_len - len(t_srl) - 4)) - 7)])
                if len(f) < len(t_err + ' ' * (block_len - len(t_err) + 6)):
                    err = ' {0}'.format(f)
                else:
                    err = ' {0}..'.format(f[0:(len(t_err + ' ' * (block_len - len(t_err) + 6))) - 7])
                localeDate = datetime.datetime.fromtimestamp(ef['errorFlags'][f]).strftime('%Y-%m-%d %H:%M')
                dte = ' {0}'.format(localeDate)
                if prev_dId != ef['deviceId']:
                    click.secho(sep + com + ' ' * (block_len - len(com) - 4) +
                                sep + sto + ' ' * (block_len - len(sto) - 4) +
                                sep + dNm + ' ' * (block_len - len(dNm) - 4) +
                                sep + srl + ' ' * (block_len - len(srl) - 4) +
                                '├' + err + ' ' * (block_len - len(err) + 6) +
                                sep + dte + ' ' * (block_len - len(dte) - 1) +
                                sep)
                else:
                    if len(f) <= len(t_err + ' ' * (block_len - len(t_err) + 6)):
                        err = ' {0}'.format(f)
                    else:
                        err = ' {0}..'.format(f[0:len(t_err + ' ' * (block_len - len(t_err) + 5))])
                    click.secho(sep + ' ' * (3 * block_len + 6) +
                                '├' + err + ' ' * (block_len - len(err) + 6) +
                                sep + dte + ' ' * (block_len - len(dte) - 1) +
                                sep)
                prev_dId = ef['deviceId']
            click.secho('├' + '─' * (row_len - 6) + '┤')
        click.echo()
    else:
        click.secho('✔ NO ERROR WAS FOUND', fg='green')


@click.command(name='device', short_help='Show devices.', context_settings={"ignore_unknown_options": True})
@click.pass_context
@click.argument('args', default=None, required=False)
@click.option('-v', '--firmware-version', help='Firmware version', is_eager=True)
@click.option('-sn', '--serial-number', help='Device serial number', default=None, is_eager=True)
@click.option('-pn', '--part-number', help='Device part number', default=None, is_eager=True)
@click.option('-id', '--device-id', help='Device id', default=None, is_eager=True)
@click.option('-n', '--device-name', help='Device name', default=None, is_eager=True)
@click.option('-c', '--company', help='Company name', default=None, is_eager=True)
@click.option('-st', '--store', help='Store name', default=None, is_eager=True)
@click.option('-stn', '--store-number', help='Store number', default=None, is_eager=True)
@click.option('-cl', '--cluster', help='Cluster name', default=None, is_eager=True)
def device(ctx, args, firmware_version, serial_number, part_number, device_id, device_name, company, store, store_number, cluster):
    """
    Show devices. Use options to filter devices list where [ARGS] can be:
    `test`: test mode devices.
    `outup`: out-of-date devices [UNAVAILABLE]
    """
    backend_service = Backend(ctx)
    if args is not None and 'test' in args:
        test_mode = '1'
    else:
        test_mode = '0'
    where = {
        "testMode": test_mode,
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
    dev_list = backend_service.get_devices_list(where)
    if dev_list and len(dev_list):
        if serial_number:
            for device in dev_list:
                comp = device['company'] if 'company' in device else ' '
                store = device['store'] if 'store' in device else ' '
                dev_name = device['deviceName'] if 'deviceName' in device else ' '
                store_number = device['storeNumber'] if 'storeNumber' in device else ' '
                sn = device['serialNumber'] if 'serialNumber' in device else ' '
                pn = device['partNumber'] if 'partNumber' in device else ' '
                inst_name = device['installerName'] if 'installerName' in device else ' '
                inst_date = device['installingDate'] if 'installingDate' in device else ' '
                firm_ver = device['firmwareVersion'] if 'firmwareVersion' in device else ' '
                firm_upd = device['firmwareUpdatedDate'] if 'firmwareUpdatedDate' in device else ' '
                firm_upd_state = device['updateState'] if 'updateState' in device else ' '
                uptodate = device['uptodate'] if 'uptodate' in device else ' '
                dev_ip = device['deviceIP'] if 'deviceIP' in device else ' '
                mac_add = device['macAddress'] if 'macAddress' in device else ' '
                door_w = device['doorWidth'] if 'doorWidth' in device else ' '
                door_h = device['deviceHeight'] if 'deviceHeight' in device else ' '
                dist_from_door = device['distanceFromDoor'] if 'distanceFromDoor' in device else ' '
                gat = ' - '.join(device['gatingParam'].split(' ')) if 'gatingParam' in device else ' '
                scen = ' - '.join(device['sceneryParam'].split(' ')) if 'sceneryParam' in device else ' '
                state = ' - '.join(device['stateParam'].split(' ')) if 'stateParam' in device else ' '
                alloc = ' - '.join(device['allocationParam'].split(' ')) if 'allocationParam' in device else ' '
                x1 = device['calibrationLine']['x1'] if _.has(device, 'calibrationLine.x1') else ' '
                y1 = device['calibrationLine']['y1'] if _.has(device, 'calibrationLine.y1') else ' '
                x2 = device['calibrationLine']['x2'] if _.has(device, 'calibrationLine.x2') else ' '
                y2 = device['calibrationLine']['y2'] if _.has(device, 'calibrationLine.y2') else ' '
                dev_id = device['deviceId'] if 'deviceId' in device else ' '
                dev_info = backend_service.get_device_info(device_id=dev_id)
                prim_key = dev_info['symmetricKeys']['primaryKey'] if _.has(
                    dev_info, 'symmetricKeys.primaryKey') else ' '
                click.secho()
                click.secho('  Company:                  {0}'.format(comp))
                click.secho('  Store:                    {0}'.format(store))
                click.secho('  Device:                   {0}'.format(dev_name))
                click.secho('  Store Number:             {0}'.format(store_number))
                click.secho('  Serial Number:            {0}'.format(sn))
                click.secho('  Part Number:              {0}'.format(pn))
                click.secho('  Installer:                {0} [{1}]'.format(inst_name, inst_date))
                click.secho('  Firmware Version:         {0} [{1}]'.format(
                    click.style(firm_ver, fg='yellow' if not uptodate else None, blink=not uptodate), firm_upd)
                )
                click.secho('  Update State:             {0}'.format(firm_upd_state))
                click.secho('  IP:                       {0}'.format(dev_ip))
                click.secho('  Mac Address:              {0}'.format(mac_add))
                click.secho('  Door Width:               {0}'.format(door_w))
                click.secho('  Device Height:            {0}'.format(door_h))
                click.secho('  Distance From Door:       {0}'.format(dist_from_door))
                click.secho('  Gating Params:            {0}'.format(gat))
                click.secho('  Scenery Params:           {0}'.format(scen))
                click.secho('  State Params:             {0}'.format(state))
                click.secho('  Allocation Params:        {0}'.format(alloc))
                click.secho(
                    '  Calibration Lines:        [x1: {0} , y1: {1}] - [x2: {2} , y2: {3}]'.format(str(x1), str(y1), str(x2), str(y2)))
                click.secho('  Device Id:                {0}'.format(dev_id))
                click.secho('  Primary Key:              {0}'.format(prim_key))
                click.secho()
        else:
            row_len = 90
            block_len = round(row_len / 7)
            sep = '│'
            t_nom = ' #   '
            t_com = ' Company'
            t_sto = ' Store'
            t_dNm = ' Device'
            t_srl = ' S/N'
            t_ver = ' Firmware Version'
            t_upd = ' Updating State'
            click.secho('╭' + '─' * (row_len + 21) + '╮')
            click.secho(sep + t_nom +
                        sep + t_com + ' ' * (block_len - len(t_com) + 2) +
                        sep + t_sto + ' ' * (block_len - len(t_sto) + 5) +
                        sep + t_dNm + ' ' * (block_len - len(t_dNm)) +
                        sep + t_srl + ' ' * (block_len - len(t_srl)) +
                        sep + t_ver + ' ' * (block_len - len(t_ver) + 5) +
                        sep + t_upd + ' ' * (block_len - len(t_upd) + 10) +
                        sep)
            click.secho('╞' + '═' * (row_len + 21) + '╡')
            count = 0
            for device in dev_list:
                dev_name = device['deviceName'] if 'deviceName' in device else ' '
                serial_number = device['serialNumber'] if 'serialNumber' in device else ' '
                comp = device['company'] if 'company' in device else ' '
                store = device['store'] if 'store' in device else ' '
                dev_name = device['deviceName'] if 'deviceName' in device else ' '
                uptodate = device['uptodate'] if 'uptodate' in device else ' '
                firm_ver = device['firmwareVersion'] if 'firmwareVersion' in device else ' '
                firm_upd_state = device['updateState'] if 'updateState' in device else ' '
                count += 1
                if len(comp) < len(t_com + ' ' * (block_len - len(t_com) + 2)):
                    company = ' {0}'.format(comp)
                else:
                    company = ' {0}..'.format(comp[0:(len(t_com + ' ' * (block_len - len(t_com) + 4)) - 3)])
                if len(store) < len(t_sto + ' ' * (block_len - len(t_sto) + 5)):
                    store = ' {0}'.format(store)
                else:
                    store = ' {0}..'.format(store[0:(len(t_sto + ' ' * (block_len - len(t_sto) + 5)) - 3)])
                if len(firm_ver) < len(t_ver + ' ' * (block_len - len(t_ver) + 5)):
                    firm_ver = '{0}'.format(firm_ver)
                else:
                    firm_ver = '{0}..'.format(firm_ver[0:(len(t_ver + ' ' * (block_len - len(t_ver) + 2)) - 3)])
                if firm_upd_state == 'successfully updated':
                    firm_upd_state = ' '
                if len(firm_upd_state) < len(t_upd + ' ' * (block_len - len(t_upd) + 10)):
                    firm_upd_state = ' {0}'.format(firm_upd_state)
                else:
                    firm_upd_state = ' {0}..'.format(
                        firm_upd_state[0:(len(t_upd + ' ' * (block_len - len(t_upd) + 10)) - 3)])

                device_name = ' {0}'.format(dev_name)
                serial_number = ' {0}'.format(serial_number)
                click.secho(sep + ' ' + str(count) + ' ' * (4 - len(str(count))) +
                            sep + company + ' ' * (block_len - len(company) + 2) +
                            sep + store + ' ' * (block_len - len(store) + 5) +
                            sep + device_name + ' ' * (block_len - len(device_name)) +
                            sep + serial_number + ' ' * (block_len - len(serial_number)) +
                            sep + ' ' + click.style(firm_ver, fg='yellow' if not uptodate else None) +
                            ' ' * (block_len - len(firm_ver) + 4) +
                            sep + click.style(firm_upd_state) + ' ' * (block_len - len(firm_upd_state) + 10) + sep
                            )
            click.secho('╰' + '─' * (row_len + 21) + '╯')
            click.echo()
    else:
        click.secho('  NO DEVICE WAS FOUND!', fg='yellow')


show.add_command(error)
show.add_command(device)
