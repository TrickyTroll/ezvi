# EZ-VI

`EZ-VI` is a python package that allows typing automation for the `Vi` editor.

## Installation

`EZ-VI` is distributed as a Pip package. To install the program, simply run

```bash
pip install ez-vi
```

## Usage

The package can be used via the `CLI`. `EZ-VI` functions can also be imported and used in a Python program.

## The `CLI`

There are two different ways of using `EZ-Vi` via the command line. 

### The `copy` command 

`copy` can be used to type a pre-written file. It takes one argument (`infile` and one option (`--writefile`).

* `infile` is the path towards the pre-written file.
* `--writefile` tells the program to save the file again after typing it. `--writefile` takes one argument that corresponds to the path where the typed file will be written.

#### Example

```bash
ez-vi copy -w ./foo.txt example/message.txt
```

This takes the `message.txt` example from the [example](https://github.com/TrickyTroll/EZ-VI/tree/latest/example) directory and types it again. The Vi buffer is then written to `./foo.txt`.

### The `script` command

`script` should be used to take a configuration as instructions to type a new file. The `script` command only takes one argument (`config`). Everything else should be specified in the config file.

* `config` is the path towards the configuration file.

#### Example

```bash
ez-vi script example/config.yaml
```

This command would take the `config.yaml` file from the [example](https://github.com/TrickyTroll/EZ-VI/tree/latest/example) directory and use it to type a new file.

## Writing a config file

A configuration file is just a yaml file that will be parsed using [PyYAML](https://pyyaml.org "PyYAML"). The structure of the file should be similar to the one in the `config.yaml` file from the [example](https://github.com/TrickyTroll/EZ-VI/tree/latest/example) directory.

```yaml
- write_line: "Hello!"
- new_line: 2
- write_chars: "-- Good Bot."
- write_file: "message.txt"
- quit_editor:
```

A `-` must precede every action.

## Development

This package is still in alpha. Not much testing has been done and many things could still change.  To see the latest commit, go check the [latest](https://github.com/TrickyTroll/EZ-VI/tree/latest) branch.
