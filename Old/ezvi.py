from funcmodule import *

# Need to remove this later. This is what the instructions should look like.
writing = {"insert":"i", "text":"foooo", "newline":"\n", "text":"bar", "escape":chr(27)}

ez_spawn("vi", writing)
print("Done")