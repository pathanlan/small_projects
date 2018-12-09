#!/usr/bin/env python3
# Reference - https://www.python-course.eu/os_module_shell.php
import subprocess, time

speakerGUID = '04:52:C7:21:CA:4A'
testSubprocess = subprocess.run(['rfcomm','connect','0',speakerGUID,'1'])