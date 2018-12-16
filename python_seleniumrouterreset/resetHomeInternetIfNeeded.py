#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import sys

from credentials import myRouterCredentials

firefox = webdriver.Firefox()

# Log in to the router admin site
firefox.get("http://192.168.0.1/start.htm")

loggedIn = False
alertWaitRetryCount = 0
while not loggedIn and alertWaitRetryCount < 3:
    try:
        wait = WebDriverWait(firefox, 2)
        wait.until(expected_conditions.alert_is_present())
        alert = firefox.switch_to.alert
        alert.send_keys(myRouterCredentials.userName + Keys.TAB + myRouterCredentials.password)
        alert.accept()
    except TimeoutException as identifier:
        loggedIn = firefox.current_url == "http://192.168.0.1/start.htm"        
        alertWaitRetryCount = alertWaitRetryCount + 1
        firefox.get("http://192.168.0.1/start.htm")

if loggedIn:
    print("Logged in to router")
elif alertWaitRetryCount == 3:
    print("Did not log in to router")
    firefox.quit()
    sys.exit(1)

# Check if the internet is connected
wait = WebDriverWait(firefox, 2)
wait.until(expected_conditions.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='page']")))
wait = WebDriverWait(firefox, 10)
wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//td[@id='internet1']/span[1]")))
statusTextSpan = firefox.find_element_by_xpath("//td[@id='internet1']/span[1]")
internetConnectionNeedsReset = str.lower(statusTextSpan.text) == "not connected"
if internetConnectionNeedsReset:
    print("Internet connection is bad, proceed with reset")    
else:
    print("Internet connection is good, no need to reset")

    # Write a timestamp and a zero to the stats file, representing no reset needed
    statsFile = open("stats.csv", "w+")
    statsFile.write("{:%Y/%m/%d %H:%M},0\r\n".format(datetime.now()))
    statsFile.close()

    firefox.quit()
    sys.exit(0)

# If the internet is not connected, go to the internet status page
firefox.get("http://192.168.0.1/RST_st_ppa.htm")
wait = WebDriverWait(firefox, 5)
wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@name='Disconnect']")))
print("Reached internet status page")

# Disconnect the internet
firefox.find_element_by_xpath("//button[@name='Disconnect']").send_keys(Keys.ENTER)
wait = WebDriverWait(firefox, 2)
wait.until(expected_conditions.alert_is_present())
alert = firefox.switch_to.alert
alert.accept()
print("Requested that the internet be disconnected")

# Connect the internet
wait = WebDriverWait(firefox, 5)
try:
    wait.until(expected_conditions.element_to_be_clickable((By.XPATH,"//button[@name='Connect']")))
except TimeoutException as identifier:
    # Sometimes there's a timeout, which occurs when the internet was 
    # Disconnected cleanly/manually outside of the script, and we get the
    # "Session not connected" page
    print("Timeout waiting for Disconnect - Internet may have been cleanly/manually disconnected previously")

    wait = WebDriverWait(firefox, 2)
    firefox.get("http://192.168.0.1/RST_st_ppa.htm")
    wait.until(expected_conditions.element_to_be_clickable((By.XPATH,"//button[@name='Connect']")))

firefox.find_element_by_xpath("//button[@name='Connect']").send_keys(Keys.ENTER)
print("Requested that the internet be connected")
wait = WebDriverWait(firefox, 10)
wait.until(expected_conditions.url_matches("http://192.168.0.1/RST_st_ppa.htm"))

# Verify the internet is connected
firefox.get("http://192.168.0.1/start.htm")
wait = WebDriverWait(firefox, 2)
wait.until(expected_conditions.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='page']")))
wait = WebDriverWait(firefox, 5)
wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//td[@id='internet1']/span[2]")))
statusTextSpan = firefox.find_element_by_xpath("//td[@id='internet1']/span[2]")
internetConnectionIsGood = str.upper(statusTextSpan.text) == "GOOD"
if internetConnectionIsGood:
    print("Internet connection is good, reset succesful")

    # Write a timestamp and a one to the stats file, representing a reset needed
    # and done successfully
    statsFile = open("stats.csv", "w+")
    statsFile.write("{:%Y/%m/%d %H:%M},1\r\n".format(datetime.now()))
    statsFile.close()

    firefox.quit()
    sys.exit(0)
else:
    print("Internet connection is bad, reset failed")
    firefox.quit()
    sys.exit(0)