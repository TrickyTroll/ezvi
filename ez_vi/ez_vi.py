from funcmodule import *
# Need to remove this later. This is what the instructions should look like.
writing = [write_chars("toto"),
            newline(),
            write_chars("hello"),
            write_file("filename.txt"),
            quit_editor()]

ez_spawn("vi", writing)
print("Done")
