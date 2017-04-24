import time
import os
import subprocess
cwd = os.getcwd()
cmd = 'git pull origin master'

while True:
  subprocess.call(cmd, shell=True)
  time.sleep(30)
