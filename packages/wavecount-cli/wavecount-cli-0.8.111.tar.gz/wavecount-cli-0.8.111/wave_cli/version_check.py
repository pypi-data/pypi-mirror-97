import math
import requests
import click
from halo import Halo

from wave_cli import VERSION, PACKAGE_NAME


class Version:
    def __init__(self, version_str):
        self.version_tuple = self._parse_version(version_str)
        pass

    def _parse_version(self, version_str):
        version = tuple(map(int, version_str.split('.')))
        if len(version) == 0:
            return [0, ]
        return version


def get_current_version():
    return Version(VERSION).version_tuple


def get_latest_version():
    pypi_url = 'https://pypi.org/pypi/{0}/json'.format(PACKAGE_NAME)
    result = requests.get(pypi_url)
    latest_version = result.json()['info']['version']
    return Version(latest_version).version_tuple


def compare():
    current_version = get_current_version()
    spinner = Halo(spinner='dots3', text_color='grey')
    try:
        spinner.start(text='Checking version')
        latest_version = get_latest_version()
        for i in range(len(current_version)):
            if latest_version[i] > current_version[i]:
                spinner.warn('out-of-date')
                cl = 60
                click.echo('\n')
                click.secho('╭' + (cl - 2) * '─' + '╮', fg='yellow')
                click.secho('│' + (cl - 2) * ' ' + '│', fg='yellow')
                avail_msg = 'Update available {} → {}'.format('.'.join(map(str, current_version)), '.'.join(map(str, latest_version)))
                click.secho('│' +
                            math.ceil((cl - 2 - len(avail_msg)) / 2) * ' ' +
                            avail_msg +
                            math.floor((cl - 2 - len(avail_msg)) / 2) * ' ' +
                            '│',  fg='yellow')
                hint_msg = click.style('Run ', fg='yellow') + \
                    click.style('pip3 install --upgrade {} '.format(PACKAGE_NAME), fg='blue') + \
                    click.style('to update', fg='yellow')
                click.secho(click.style('│', fg='yellow') +
                            math.floor((cl - 2 - 50) / 2) * ' ' +
                            hint_msg +
                            math.floor((cl - 2 - 50) / 2) * ' ' +
                            click.style('│', fg='yellow')
                            )
                click.secho('│' + (cl - 2) * ' ' + '│', fg='yellow')
                click.secho('╰' + (cl - 2) * '─' + '╯', fg='yellow')
                click.secho()
                return latest_version
            else:
                continue
        spinner.succeed('up-to-date')
        return None
    except requests.ConnectionError as e:
        spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
        exit()
    except requests.Timeout as e:
        spinner.fail(text='oops!! Timeout Error')
        exit()
    except requests.RequestException as e:
        spinner.fail(text='oops!! General Error')
        exit()
    except KeyboardInterrupt:
        spinner.fail(text='someone closed the program')
