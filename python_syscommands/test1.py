#!/usr/bin/env python3
import subprocess, time

# Constant values
speakerGUID = '04:52:C7:21:CA:4A'
connectionTimeoutPeriod = 5.0

# Connect to a new instance of the "bluetoothctl" process
bluetoothctlProcess = subprocess.Popen(['bluetoothctl'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

# Monitor the output from the process until we can tell it's ready
# to receive messages, and then send a connect message
lastCharacterReadFromProcessOutput = ''
processReadyToReceiveMessage = False
connectMessageSent = False
lastFullLineReceived = ''
while connectMessageSent == False: # Keep looping until the process is ready, and we've sent the message
    lastCharacterReadFromProcessOutput = bluetoothctlProcess.stdout.read(1).decode("unicode_escape")
    lastFullLineReceived = lastFullLineReceived + lastCharacterReadFromProcessOutput

    if lastCharacterReadFromProcessOutput == '#' and processReadyToReceiveMessage == True:
        connectMessage = "connect {}\n".format(speakerGUID)
        bluetoothctlProcess.stdin.write(connectMessage.encode())
        bluetoothctlProcess.stdin.flush()
        connectMessageSent = True

    elif lastCharacterReadFromProcessOutput == "\n":
        lastFullLineReceived = lastFullLineReceived.rstrip("\n")
        if lastFullLineReceived.find("Agent registered") >= 0:  # If we receive this message, the process has started and 
                                                                # is ready to receive messages
            processReadyToReceiveMessage = True
        lastFullLineReceived = ''

# Now we wait until the process lets us know if it was able to connect or not
lastFullLineReceived = ''
startTime = time.time()
while True:
    lastCharacterReadFromProcessOutput = bluetoothctlProcess.stdout.read(1).decode("unicode_escape")
    lastFullLineReceived = lastFullLineReceived + lastCharacterReadFromProcessOutput

    if lastCharacterReadFromProcessOutput == "\n":
        lastFullLineReceived = lastFullLineReceived.rstrip("\n")
        if lastFullLineReceived.find("Connection successful") >= 0:
            print("Connected to speaker")
            break
        elif lastFullLineReceived.find("Failed") >= 0:
            print("Did not connect to speaker")
            break
        elif (time.time() - startTime) > connectionTimeoutPeriod:
            print("Bluetoothctl did not respond within the timeout period")
        else:
            lastFullLineReceived = ''

bluetoothctlProcess.terminate()
bluetoothctlProcess.wait()