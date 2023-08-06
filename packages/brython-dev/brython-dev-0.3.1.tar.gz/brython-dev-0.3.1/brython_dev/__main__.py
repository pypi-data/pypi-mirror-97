import click
from flask import Flask, current_app
from flask.cli import FlaskGroup
from flask.cli import with_appcontext

from flask_threaded_sockets import ThreadedWebsocketServer

from brython_dev import __version__, create_app


@click.group(cls=FlaskGroup, create_app=create_app, add_version_option=False, add_default_commands=True)
@click.version_option(version=__version__)
def cli():
    """Management script for brython developers."""    

@cli.command(short_help="Run the server.")
@click.option("--host", "-h", default="127.0.0.1", help="The interface to bind to.")
@click.option("--port", "-p", default=5000, help="The port to bind to.")
@with_appcontext
def run(host, port):
    """Run the server."""
    # app = create_app()
    # click.echo(f"* Proyect Name: {app.config['NAME']}")
    # click.echo(f"* Configuration:")
    # click.echo(f"    Main App: {app.config['APP']}")
    # click.echo(f"    Main Template: {app.config['TEMPLATE']}")
    # click.echo(f"    Use Brython: {app.config['USE_BRYTHON']}")
    # click.echo(f"    Use Brython Stdlib: {app.config['USE_BRYTHON_STDLIB']}")
    # click.echo(f'* Running on http://{host}:{port}/ (Press CTRL+C to quit)')
    
    # with current_app.app_context():
    # ThreadedWebsocketServer(host, port, app).serve_forever()
    # click.echo(f'* Stop the server')

cli(prog_name="Bython-dev")
