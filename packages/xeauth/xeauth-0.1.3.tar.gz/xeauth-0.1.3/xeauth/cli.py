"""Console script for xeauth."""
import sys
import xeauth
import click


@click.command()
def main():
    """Console script for xeauth."""
    click.echo("Replace this message by putting your code into "
               "xeauth.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0

@click.command()
def login():
    xeauth.cli_login()

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
