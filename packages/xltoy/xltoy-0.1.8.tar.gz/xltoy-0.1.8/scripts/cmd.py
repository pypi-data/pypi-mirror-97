# -*- coding: utf-8
"""
xltoy main cli (Command Line Interface)
"""
import click
from xltoy.collector import Collector, DiffCollector
from xltoy.utils import timeit
from xltoy import *

def set_verb(v=0):
    """
    Set logging verbosity

    :param v:  verbosity 1:WARNING,
                         2:INFO,
                         3+:DEBUG
    :return: Nothing, but logging verbosity was set
    """
    if v>2:
        log.setLevel(DEBUG)
    elif v>1:
        log.setLevel(INFO)
    else:
        log.setLevel(WARNING)

@click.group()
def cli():
    pass

@click.command()
@click.option('--timeit', is_flag=True, help='Print out how many times it takes for the task')
@click.option('--yaml', is_flag=True, help='Print out the yaml hierarchical view')
@click.option('--json', is_flag=True, help='Print out the json hierarchical view')
@click.option('--gml_graph', type=click.Path(exists=False), help='save to a file the topology of models in gml format')
@click.option('--data', is_flag=True, help='Collect only data, it will ignore formulas')
@click.option('-v', '--verbose', count=True, help="verbose output (repeat for increased verbosity)")
@click.option('--add_fingerprint', is_flag=True, help='Add metadata under section xltoy')
@click.option('--parsed', is_flag=True, help='Parse formulas and use this version instead of excel syntax')
@click.argument('filename')
def collect(filename, **kwargs):
    set_verb(kwargs.get('verbose'))
    with timeit("{} collect".format(filename), kwargs.get('timeit')):

        if kwargs.get('gml_graph'):
            kwargs['parsed'] = True

        c = Collector(filename,
                      only_data=kwargs.get('data'),
                      parsed=kwargs.get('parsed'),
                      add_fingerprint=kwargs.get('add_fingerprint'),
                      )

        if kwargs.get('yaml'):
            with timeit("pseudo to yaml"):
                print(c.to_yaml())

        elif kwargs.get('json'):
            with timeit("pseudo to json"):
                print(c.to_json())

        if kwargs.get('gml_graph') is not None:
            c.store_gml(kwargs['gml_graph'])




@click.command()
@click.option('--timeit', is_flag=True, help='Print out how many times it takes for the task')
@click.option('--data', is_flag=True, help='Collect only data, it will ignore formulas')
@click.option('--relative', is_flag=True, help='Areas are handled as relative, each starts from row1,col1')
@click.option('-v', '--verbose', count=True, help="verbose output (repeat for increased verbosity)")
@click.option('--add_fingerprint', is_flag=True, help='Add metadata under section xltoy')
@click.option('--parsed', is_flag=True, help='Parse formulas and use this version instead of excel syntax')
@click.option('--json', is_flag=True, help='Print out in json format instead of default YAML')
@click.argument('filename1')
@click.argument('filename2')
def diff(filename1, filename2, **kwargs):
    set_verb(kwargs.get('verbose'))
    with timeit("collect 2 files", kwargs.get('timeit')):
        d = DiffCollector(filename1,filename2,
                          only_data=kwargs.get('data'),
                          relative=kwargs.get('relative'),
                          parsed=kwargs.get('parsed'),
                          add_fingerprint=kwargs.get('add_fingerprint'))
        if kwargs.get('json'):
            d.to_json()
        else:
            d.to_yaml()

cli.add_command(collect)
cli.add_command(diff)

if __name__ == '__main__':
    cli()
