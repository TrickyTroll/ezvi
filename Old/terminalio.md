---
tile: Notes on terminal I/O
author: Etienne Parent
date: today
---
# Notes on terminal I/O from Advanced Programming in the UNIX Environment

## Overview

### Canonical mode

- Terminal input is processed as lines.

### Non-canonical mode

- Input characters are not assembled into lines.
- Programs that manipulate the entire screen use the non-canonical mode because
the commands can be single characters and do not have to end with a newline.

## Special Input Characters
