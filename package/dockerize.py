import click
import pkgutil

@click.command()
def cli():
    """Example script."""
    click.echo('Generating Dockerfile')
    text = pkgutil.get_data(__name__, "templates/Java.Dockerfile").decode()
    open("Dockerfile", "w").writelines([l for l in text])
