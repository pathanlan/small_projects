#!/usr/bin/env python3
# Reference - https://www.python-course.eu/os_module_shell.php
import subprocess, time

speakerGUID = '04:52:C7:21:CA:4A'
testSubprocess = subprocess.Popen(['bluetoothctl'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

# Reference - https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python
line = ''
lastChar = ''
isReady = False
sent = False
while sent == False:  # lets wait for 'user' prompt
    lastChar = testSubprocess.stdout.read(1).decode("unicode_escape")
    line = line + lastChar
    if isReady == True:
        if lastChar == '#':
            print(line)
            commandString = "connect {}\n".format(speakerGUID)
            print(commandString)
            testSubprocess.stdin.write(commandString.encode())
            testSubprocess.stdin.close()
            isReady = False
            print(testSubprocess.poll())
            sent = True
    elif lastChar == '\n':
        line = line.rstrip('\n')
        if line.find('Agent registered') >= 0:
            isReady = True
        print(line)
        line = ''
    #if line.find('Agent registered') >= 0:
        # https://stackoverflow.com/questions/510348/how-can-i-make-a-time-delay-in-python
    #    time.sleep(2)
    #    testSubprocess.stdin.write('connect {}\n'.format(speakerGUID).encode())
