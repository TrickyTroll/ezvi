from funcmodule import *
# Need to remove this later. This is what the instructions should look like.
writing = {"insert": "i", 
            "allo":"bye", 
            "foo":"bar", 
            "newline":"\n", 
            "toto":"tata", 
            "escape":chr(27),
            "write": ":w toto.txt",
            "eter": "\n", 
            "command": ":q!",
            "enter": "\n"}

ez_spawn("vi", writing)
print("Done")