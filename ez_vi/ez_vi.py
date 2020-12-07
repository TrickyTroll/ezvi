from funcmodule import *

# Need to remove this later. This is what the instructions should look like.
writing = [write_chars("Helloooo"),
           newline(),
           write_chars("This is a message"),
           newline(),
           newline(),
           write_chars("-- Good Bot"),
           write_file("filename.txt"),
           quit_editor()]

ez_spawn(("vi",), writing)
print("Done")
