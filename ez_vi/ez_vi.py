from funcmodule import *
import click

with open("../example/config.yaml") as stream:
    parsed = yaml_parser(stream)

writing = []
for item in parsed:
    for key in item:
        writing.append(item[key])

ez_spawn(("vi",), writing)
print("Done")
