# ezvi

`ezvi` is a python package that allows typing automation for the `Vi` editor.

## Installation

`ezvi` is distributed as a Pip package. To install the program, simply run

```bash
pip install ezvi
```

## Usage

The package can be used via the `CLI`. `ezvi` functions can also be imported and used in a Python program.

## The `CLI`

There are two different ways of using `EZ-Vi` via the command line. 

### The `text` command 

`text` can be used to type a pre-written file. It takes one argument (`infile` and one option (`--writefile`).

* `infile` is the path towards the pre-written file.
* `--writefile` tells the program to save the file again after typing it. `--writefile` takes one argument that corresponds to the path where the typed file will be written.

#### Example

```bash
ezvi text -w ./foo.txt example/message.txt
```

This takes the `message.txt` example from the [example](https://github.com/TrickyTroll/ezvi/tree/latest/example) directory and types it again. The Vi buffer is then written to `./foo.txt`.

### The `yaml` command

`yaml` should be used to take a configuration as instructions to type a new file. The `yaml` command only takes one argument (`config`). Everything else should be specified in the config file.

* `config` is the path towards the configuration file.

#### Example

```bash
ezvi yaml example/config.yaml
```

This command would take the `config.yaml` file from the [example](https://github.com/TrickyTroll/ezvi/tree/latest/example) directory and use it to type a new file.

## Writing a config file

A configuration file is just a yaml file that will be parsed using [PyYAML](https://pyyaml.org "PyYAML"). The structure of the file should be similar to the one in the `config.yaml` file from the [example](https://github.com/TrickyTroll/ezvi/tree/latest/example) directory.

```yaml
- write_line: "Hello!"
- new_line: 2
- write_chars: "-- Good Bot."
- write_file: "message.txt"
- quit_editor:
```

A `-` must precede every action.

## Development

This package is still in alpha. Not much testing has been done and many things could still change.  To see the latest commit, go check the [latest](https://github.com/TrickyTroll/ezvi/tree/latest) branch.
