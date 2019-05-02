from src.server.instance import server
from src import setup
import sys, os

# Need to import all resources
# so that they register with the server 
from src.resources.property import *
from src.resources.entity import *
import click

@server.app.cli.command()
def setupall():
    setup.create_model()
    setup.create_indexer()

@server.app.cli.command()
def createmodel():
    setup.create_model()

@server.app.cli.command()
def createindex():
    setup.create_indexer()

@server.app.cli.command()
@click.argument('index_name')
def updateindex(index_name):
    setup.delete_index(index_name)
    setup.dumping_property()
    setup.create_indexer()
