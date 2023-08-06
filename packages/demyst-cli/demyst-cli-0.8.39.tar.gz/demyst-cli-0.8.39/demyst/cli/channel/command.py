import os
import click
from tabulate import tabulate
from demyst.common.config import load_config

@click.group()
def channel():
    pass

@channel.command()
@click.option('--config_file', default=None, required=False, help='Config file or ./demyst.config')
@click.option('--username', default=None, required=False, help='Username.')
@click.option('--password', default=None, required=False, help='Password.')
@click.option('--key', default=None, required=False, help='API key.')
@click.option('--env', default="prod", required=False, help='Environment (stg or prod).')
def list(config_file, username, password, key, env):
    if(env == 'dev'):
        region = 'local'
    else:
        region = 'us'
    """List all channels belonging to org."""
    config = load_config(config_file=config_file, username=username, password=password, key=key, env=env, region=region)

    url = config.get('MANTA_URL') + 'channels'
    resp = config.auth_get(url)
    channels = resp.json()

    table = []
    headers = ['ID', 'Name', 'Region', 'Pipes', 'Data Functions', 'Protected']
    for channel in channels:
        dfs = [pipe['data_function_name'] for pipe in channel['pipes']]
        num_dfs = sum(df is not None for df in dfs)
        channels[0]['pipes'][0]['data_function_name']
        table.append([channel['id'], channel['name'], channel['region'], len(channel['pipes']), num_dfs, channel['protected']])
    click.echo(tabulate(table, headers, tablefmt="presto"))

@channel.command()
@click.option('--channel_id', default=None, required=True, help='ID of channel.')
@click.option('--config_file', default=None, required=False, help='Config file or ./demyst.config')
@click.option('--username', default=None, required=False, help='Username.')
@click.option('--password', default=None, required=False, help='Password.')
@click.option('--key', default=None, required=False, help='API key.')
@click.option('--env', default="prod", required=False, help='Environment (stg or prod).')
def view(channel_id, config_file, username, password, key, env):
    """List all pipes belonging to channel."""
    if(env == 'dev'):
        region = 'local'
    else:
        region = 'us'
    config = load_config(config_file=config_file, username=username, password=password, key=key, env=env, region=region)
    url = config.get('MANTA_URL') + 'channels/{}'.format(channel_id)
    try:
        resp = config.auth_get(url)
    except:
        raise RuntimeError("It looks like you do not have permissions to perform this action. Please ensure you entered the correct Channel ID.\nContact support@demystdata.com for help.")
    channel = resp.json()
    pipes = channel['pipes']

    table = []
    headers = ['Pipe ID', 'Status', 'Pipe Name', 'Providers', 'Data Functions']
    for pipe in pipes:
        if pipe['active']:
            status = 'active'
        else:
            status = 'inactive'
        providers = ", ".join([version['provider_name'] for version in pipe['provider_versions']])
        table.append([pipe['id'], status, pipe['name'], providers, pipe['data_function_name']])
    click.echo(tabulate(table, headers, tablefmt="presto"))

@channel.command()
@click.option('--config_file', default=None, required=False, help='Config file or ./demyst.config')
@click.option('--username', default=None, required=False, help='Username.')
@click.option('--password', default=None, required=False, help='Password.')
@click.option('--key', default=None, required=False, help='API key.')
@click.option('--env', default="prod", required=False, help='Environment (stg or prod).')
@click.option('--name', default=None, required=True, help='Name for channel')
@click.option('--region', default="us", required=True, help='Region.')
@click.option('--timeout', default=60, required=False, help='Timeout length in seconds.')
@click.option('--protected', default=True, required=False, help='Channel is protected (True/False)/')
def create(config_file, username, password, key, env, name, region, timeout, protected):
    if(env == 'dev'):
        config_region = 'local'
    else:
        config_region = 'us'
    config = load_config(config_file=config_file, username=username, password=password, key=key, env=env, region=config_region)
    regions = config.auth_get(config.get("MANTA_URL") + "list_regions").json()

    region_codes = [region['code'] for region in regions]
    region_arr = [region_data for region_data in regions if region_data['code'] == region]
    if len(region_arr) == 1:
        region_id = region_arr[0]["id"]
    else:
        raise RuntimeError("Invalid region code. Your regions are {}.".format((", ").join(region_codes)))

    url = config.get('MANTA_URL') + 'v1/channels'
    params = {"channel" : {"name" : name, "timeout":timeout, "provider_timeout_seconds":timeout, "protected": protected, "region":region}}
    resp = config.auth_post(url, json=params).json()
    headers = ['ID', 'Name', 'Region', 'Timeout (s)', 'Protected']
    data = [resp['id'], resp['name'], region, resp['provider_timeout_seconds'], resp['protected']]
    click.echo(tabulate([data], headers, tablefmt="presto"))

@channel.command()
@click.option('--config_file', default=None, required=False, help='Config file or ./demyst.config')
@click.option('--username', default=None, required=False, help='Username.')
@click.option('--password', default=None, required=False, help='Password.')
@click.option('--key', default=None, required=False, help='API key.')
@click.option('--env', default="prod", required=False, help='Environment (stg or prod).')
@click.option('--channel_id', default=None, required=True, help='The ID of the channel you would like to delete.')
def delete(config_file, username, password, key, env, channel_id):
    if(env == 'dev'):
        config_region = 'local'
    else:
        config_region = 'us'
    config = load_config(config_file=config_file, username=username, password=password, key=key, env=env, region=config_region)
    url = config.get('MANTA_URL') + 'channels/{}'.format(channel_id)
    try:
        resp = config.auth_get(url)
    except:
        raise RuntimeError("It looks like you do not have permissions to perform this action. Please ensure you entered the correct Channel ID.\nContact support@demystdata.com for help.")
    channel_data = resp.json()
    channel_name = channel_data['name']
    click.confirm('Are you sure you want to delete Channel {}, {}?'.format(channel_id, channel_name), abort=True)
    url = config.get('MANTA_URL') + 'v1/channels/{}/delete'.format(channel_id)
    resp = config.auth_post(url).json()
    if resp['success']:
        click.echo("Successfully Deleted Channel {}".format(channel_id))
