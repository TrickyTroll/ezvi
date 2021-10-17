"""
The CLI module. Contains every command used by ``ezvi``.
No function other than the command line options should be
defined in this module.
"""
import click
from ezvi import funcmodule


@click.group()
def app():
    """A tool to automate typing in the Vi editor"""


@click.command()
@click.argument(
    "infile",
    type=click.File("r"),
)
@click.option(
    "-w",
    "--writefile",
    type=str,
    help="""\
    To save the newly created file. 
    Use `ezvi text -w [NEW_PATH] [PATH_TO_EXISTING_FILE]`.
    """,
)
def text(infile, writefile):
    """
    To re-type an already pre-typed file. `ezvi` will just rewrite the
    file as-is character by character.
    """
    if not writefile:
        writing = funcmodule.file_parser(infile)
    else:
        writing = funcmodule.file_parser(infile, name=writefile)

    funcmodule.ez_spawn(("vi",), writing)


@click.command()
@click.argument(
    "config",
    type=click.File("r"),
)
def yaml(config):
    """To use a YAML config file as input."""

    parsed = funcmodule.yaml_parser(config)
    writing = []
    for item in parsed:
        for key in item:
            writing.append(item[key])

    funcmodule.ez_spawn(("vi",), writing)


@click.command()
@click.argument(
    "infile",
    type=click.File("r"),
)
@click.option(
    "-s",
    "--savepath",
    type=str,
    help="""\
        To save the config file.
        This is the path towards where the file will be saved.
        """,
)
def create_config(infile, savepath):
    """To generate a config file."""
    if savepath:
        funcmodule.new_conf(infile, savepath)
    else:
        for line in infile:
            line = line.strip()
            if not line:
                to_echo = "- new_line: "
            else:
                to_echo = "- write_line: " + line
            click.echo(to_echo)


app.add_command(create_config)
app.add_command(yaml)
app.add_command(text)


def main():
    app()
