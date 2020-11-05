#!/usr/bin/env python3

import subprocess
import time
import os


vi = subprocess.Popen(["vi", "-", "toto.txt"],
                      stdin = subprocess.PIPE)
#                      stdout = subprocess.PIPE,
#                      stderr = subprocess.PIPE)
time.sleep(1)
vi.kill()
# Clearing prompt
print("\n")
subprocess.run("reset")
os.system('cls' if os.name == 'nt' else 'clear')
