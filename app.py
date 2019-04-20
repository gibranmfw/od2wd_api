from src.server.instance import server
from src import setup
import sys, os

# Need to import all resources
# so that they register with the server 
from src.resources.property import *
from src.resources.entity import *
import click

@server.app.cli.command()
def setup_all():
    setup.create_model()
    setup.dumping_property()
    setup.create_indexer()

@server.app.cli.command()
def create_model():
    setup.create_model()

@server.app.cli.command()
def dump_property():
    setup.dumping_property()

@server.app.cli.command()
def create_index():
    setup.create_indexer()
