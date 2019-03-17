import pyfiglet
import click
from init.init import init


@click.group()
def cli():
    pyfiglet.print_figlet("Azor C")
    pass


cli.add_command(init)
