import os

from pymongo import MongoClient
import click
from flask import current_app, g


def get_db():
    if 'client' not in g:
        g.client = MongoClient(current_app.config['DATABASE'])
    
    if 'db' not in g:
        g.db = g.client.get_database('WhatsUp')

    return g.db

def close_client(e=None):
    client = g.pop('client', None)

    if client is not None:
        client.close()

def init_collections():
    db = get_db()
    
    db.create_collection('images', check_exists=False)
    db.create_collection('messages', check_exists=False)
    db.create_collection('posts', check_exists=False)
    db.create_collection('profile_information', check_exists=False)
    db.create_collection('settings', check_exists=False)
    db.create_collection('users', check_exists=False)

    close_client()

@click.command('init-collections')
def init_collections_command():
    """Clear the existing data and create new tables."""
    init_collections()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_client)
    app.cli.add_command(init_collections_command)
