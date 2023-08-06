import click
from utils.zk import show_zk_config, set_zk_key, del_zk_key
from colorama import init


@click.group()
def cli():
    pass


@click.command()
@click.argument('service_name', nargs=1)
@click.argument('stage', nargs=1)
def show(service_name, stage):
    show_zk_config(service_name, stage)


@click.command()
@click.argument('service_name', nargs=1)
@click.argument('stage', nargs=1)
@click.argument('key', nargs=1)
@click.argument('value_type', nargs=1)
@click.argument('value', nargs=1)
def setkey(service_name, stage, key, value_type, value):
    set_zk_key(service_name, stage, key, value_type, value)


@click.command()
@click.argument('service_name', nargs=1)
@click.argument('stage', nargs=1)
@click.argument('key', nargs=1)
def delkey(service_name, stage, key):
    del_zk_key(service_name, stage, key)


cli.add_command(show)
cli.add_command(setkey)
cli.add_command(delkey)

if __name__ == '__main__':
    init(autoreset=True)
    cli()
    init(autoreset=True)
