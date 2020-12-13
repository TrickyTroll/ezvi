import click

from funcmodule import ez_spawn, yaml_parser, file_parser


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
    To save the newly created file. Use `ez-vi copy -w [YOUR_PATH]`.
    '''
)
def copy(infile, writefile):
    """
    To re-type an already pre-typed file. `ez-vi` will just rewrite the
    file as-is character by character.
    """
    if not writefile:
        writing = file_parser(infile)
    else:
        writing = file_parser(infile, name=writefile)

    ez_spawn(("vi",), writing)
    return None





@click.command()
@click.argument(
    "config",
    type=click.File('r'),
)

def script(config):
    """To use a YAML config file as input."""

    parsed = yaml_parser(config)
    writing = []
    for item in parsed:
        for key in item:
            writing.append(item[key])

    ez_spawn(("vi",), writing)

app.add_command(script)
app.add_command(copy)

if __name__ == "__main__":
    app()