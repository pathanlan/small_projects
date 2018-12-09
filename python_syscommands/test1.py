#!/usr/bin/env python3
# Reference - https://www.python-course.eu/os_module_shell.php

import subprocess

# Reference - https://stackoverflow.com/questions/3172470/actual-meaning-of-shell-true-in-subprocess
testSubprocess = subprocess.Popen(['bluetoothctl'])
testSubprocess.communicate('exit')

# Reference - https://stackoverflow.com/questions/4084322/killing-a-process-created-with-pythons-subprocess-popen
testSubprocess.terminate()