import time

from progress.spinner import Spinner
import click
import requests
from typing import Optional
import os
from configparser import ConfigParser
from pathlib import Path


CONFIG_FILE_LOCATION = os.path.join(Path.home(), 'hostypage.ini')


def get_config():
    config = ConfigParser()

    if not os.path.exists(CONFIG_FILE_LOCATION):
        config.add_section('main')
        config.set('main', 'api_root', 'https://hosty.page')
        with open(CONFIG_FILE_LOCATION, 'w') as f:
            config.write(f)

    config.read(CONFIG_FILE_LOCATION)
    return config


def write_to_config(key: str, value: str, section: str = 'main') -> None:
    config = get_config()
    config.set(section, key, value)
    with open(CONFIG_FILE_LOCATION, 'w') as f:
        config.write(f)


def read_from_config(key: str, section: str = 'main', fallback=None):
    config = get_config()
    return config.get(section, key, fallback=fallback)


def get_api_key(api_key: Optional[str] = None):
    if api_key:
        return api_key

    config = get_config()
    return config.get('main', 'api_key', fallback=None)


@click.group()
def handler():
    pass


@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--api-key', default=None, required=False, help='(Optional) Your API key. Can also be set globally using the set-api-key command')
@click.option('--subdomain', default=None, required=False, help='(Optional, Pro accounts only) The subdomain to publish to')
@click.option('--domain', default=None, required=False, help='(Optional, Pro accounts only) The domain to publish to. Must be a custom domain that your have create and verified in the Hosty.Page dashboard')
@click.option('--expiry', type=click.INT, help='(Optional, Pro accounts only) The time to wait, in hours, before the site is deleted')
@click.option('--no-expiry', is_flag=True, help='(Optional, Pro accounts only) Sites never expire. Cannot be passed with the `expiry` option')
def publish(
    file: str,
    api_key: Optional[str] = None,
    subdomain: Optional[str] = None,
    domain: Optional[str] = None,
    expiry: Optional[int] = None,
    no_expiry: Optional[bool] = None,
):
    """
    Publish a HTML file or a zip containing a static site to Hosty.Page

    FILE is the local path to the file to be published
    """
    if expiry and no_expiry:
        click.secho(
            'You cannot pass the expiry and --no-expiry parameters on the same request',
            fg='red'
        )
        return

    host = read_from_config('api_root')
    api_path = 'api/site'
    click.secho(f'Pushing file {file} to HostyPage', fg='green')
    session = requests.Session()

    api_key = get_api_key(api_key)

    if api_key:
        session.headers.update(dict(Authorization=f'Token {api_key}'))

    payload = dict()

    if subdomain:
        payload['subdomain'] = subdomain

    if domain:
        payload['custom_domain'] = domain

    if expiry:
        payload['expiry'] = f'{expiry}:00:00'

    elif no_expiry:
        payload['no_expiry'] = True

    path = os.path.abspath(file)
    with open(path, 'rb') as upload_file:
        files = dict(file=upload_file)
        response = session.post(f'{host}/{api_path}', payload, files=files)

    try:
        assert response.status_code == 201
        click.secho(
            'Request completed successfully - Building site, please wait', fg='green'
        )
    except AssertionError:
        if response.status_code == 400:
            click.secho(
                f'Request failed due to error(s) is the following fields:\n{response.json()}',
                fg='red'
            )
            return
        click.secho(f'Request failed due to error(s): {response.content}', fg='red')
        return

    data = response.json()
    status = data['status']
    pk = data['id']

    spinner = Spinner('Publishing, please wait... ')
    status_errors = 0

    while status != 'Deployed':
        spinner.next()
        time.sleep(0.3)
        response = session.get(f'{host}/{api_path}/{pk}')

        try:
            assert response.status_code == 200
        except AssertionError:
            status_errors += 1
            continue

        if status_errors > 5:
            click.secho(
                f'Error fetching status from Hosty.Page: {response.content}', fg='red'
            )
            return

        status = response.json()['status']

    spinner.finish()

    click.secho(f'Deployment complete! Your site is live at {data["url"]}.', fg='green')


@click.command()
@click.argument('api_key')
def set_api_key(api_key):
    """
    Store your API key locally to the local Hosty.Page config, so that you don't have to pass `--api-key blah` with
    every request
    """
    write_to_config('api_key', api_key)
    click.secho('Successfully saved API key to config', fg='green')


@click.command()
@click.argument('api_host')
def set_api_host(api_host):
    """
    FOR TESTING PURPOSES ONLY - DON'T DO THIS!

    Lets you specify a non-standard Hosty.Page URL
    """
    write_to_config('api_root', api_host)
    click.secho('Successfully saved API host to config', fg='green')


handler.add_command(publish)
handler.add_command(set_api_key)
handler.add_command(set_api_host)

if __name__ == '__main__':
    handler()
