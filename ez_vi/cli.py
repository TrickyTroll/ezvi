import click


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


    :param infile: The input file.
    :param save: The path to save the newly typed file.
    :return: None
    """
