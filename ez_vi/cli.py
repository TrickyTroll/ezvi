import click

from ez_vi.funcmodule import ez_spawn, yaml_parser, file_parser


@click.group()
def app():
    """A tool to automate typing in the Vi editor"""
    pass


@click.command()
@click.argument(
    "infile",
    type=click.File('r'),
    help="""\
    The file you want to copy from.
    """,
)
@click.option(
    "-s",
    "--save",
    type=str,
    help='''\
    To save the newly created file. Use `ez-vi copy -s [YOUR_PATH]`.
    '''
)
def copy(infile, save):
    """
    To re-type an already pre-typed file. `ez-vi` will just rewrite the
    file as-is character by character.

    :param infile: The input file.
    :param save: The path to save the newly typed file.
    :return: None
    """
    writing = file_parser(infile)

    ez_spawn(("vi",), writing)
    return None





@click.command()
@click.argument(
    "config",
    type=click.File('r'),
    help="""\
    The file you want to copy from.
    """,
)
def script(config):
    """To use a YAML config file as input.

    :param config: The config file.
    :return: None
    """

    parsed = yaml_parser(config)
    writing = []
    for item in parsed:
        for key in item:
            writing.append(item[key])

    ez_spawn(("vi",), writing)


