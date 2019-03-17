import pyfiglet
import click


@click.group()
def cli():
    pass


if __name__ == '__main__':
    pyfiglet.print_figlet("Azor C")
