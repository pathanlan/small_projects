#!/usr/bin/env python3
# Reference - https://www.python-course.eu/os_module_shell.php
import subprocess, time

speakerGUID = '04:52:C7:21:CA:4A'
testSubprocess = subprocess.Popen(['bluetoothctl'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

# Reference - https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python
while True:  # lets wait for 'user' prompt
    line = testSubprocess.stdout.readline().decode("unicode_escape")
    print(line)
    if line.find('Agent registered') >= 0:
        # https://stackoverflow.com/questions/510348/how-can-i-make-a-time-delay-in-python
        time.sleep(2)
        testSubprocess.stdin.write('connect {}\n'.format(speakerGUID).encode())