import click
from ezvi import funcmodule


@click.group()
def app():
    """A tool to automate typing in the Vi editor"""
    pass


@click.command()
@click.argument(
    "infile",
    type=click.File('r'),
)
@click.option(
    "-w",
    "--writefile",
    type=str,
    help='''\
    To save the newly created file. 
    Use `ez-vi text -w [NEW_PATH] [PATH_TO_EXISTING_FILE]`.
    '''
)
def text(infile, writefile):
    """
    To re-type an already pre-typed file. `ez-vi` will just rewrite the
    file as-is character by character.
    """
    if not writefile:
        writing = funcmodule.file_parser(infile)
    else:
        writing = funcmodule.file_parser(infile, name=writefile)

    funcmodule.ez_spawn(("vi",), writing)
    return None


@click.command()
@click.argument(
    "config",
    type=click.File('r'),
)
def yaml(config):
    """To use a YAML config file as input."""

    parsed = funcmodule.yaml_parser(config)
    writing = []
    for item in parsed:
        for key in item:
            writing.append(item[key])

    funcmodule.ez_spawn(("vi",), writing)


app.add_command(yaml)
app.add_command(text)

def main():
    app()