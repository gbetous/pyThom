#!/usr/bin/python

####################################################################
# This program is free software. It comes without any warranty, to #
# the extent permitted by applicable law. You can redistribute it  #
# and/or modify it under the terms of the Do What The Fuck You Want#
# To Public License, Version 2, as published by Sam Hocevar. See   #
# http://sam.zoy.org/wtfpl/COPYING for more details.               #
####################################################################

import getpass
import sys
import telnetlib
import time

#
# Customise for your needs
#
HOST = "192.168.0.254"
USER = "Administrator"
PASSWORD = ""

#
# Global definition
#
CONNECTION_STATE = "" # up OR down
CONNECTION_TYPE = "" # ADSL 
CONNECTION_BANDWIDTH = "" # "<up>/<down>" 
ATT_DOWN = "xx.x"
ATT_UP = "xx.x"
SW_VERSION = ""

#
# process_arg
#
# reads command line arguments and sets application configuration
#
def process_arg():
  for arg in sys.argv:
    print arg


#
# login
#
# sends login and password to telnet connection 
#
def login(tn):
  tn.read_until("Username : ",5)
  tn.write(USER + "\r")
  tn.read_until("Password : ",5)
  tn.write(PASSWORD + "\r")

  # Wait for the prompt
  try:
    tn.read_until("=>")
  except:
    print "Could not connect to modem ("+USER+")"

#
# close_connection
#
# closes conection 
#
def close_connection(tn):
  # Quitting
  tn.write("exit\r")
  tn.read_all()

def version(tn):
   # Get xdsl info 
  tn.write("software version\r")
  # Wait for the prompt
  ret=tn.read_until("=>")

  for line in ret.splitlines():
    if "Active" in line:
      global SW_VERSION
      SW_VERSION=line.split()[3]
      print SW_VERSION

#
# check_DSL
#
# return TRUE if connected 
#
def check_DSL(tn):
  # Get xdsl info 
  tn.write("xdsl info \r")
  # Wait for the prompt
  ret=tn.read_until("=>")

  for line in ret.splitlines():
    if "Modem state" in line:
      global CONNECTION_STATE
      CONNECTION_STATE=line.split()[2]
    if "xDSL Type" in line:
      global CONNECTION_TYPE
      CONNECTION_TYPE=line.split()[2]
    if "Bandwidth" in line:
      global CONNECTION_BANDWIDTH
      CONNECTION_BANDWIDTH=line.split()[4]

  # Get more infos if connected
  if CONNECTION_STATE == "up":
    # Get xdsl info 
    tn.write("xdsl info expand=enabled\r")
    # Wait for the prompt
    ret=tn.read_until("=>")
    for line in ret.splitlines():
      if "Attenuation" in line:
	global ATT_DOWN
        ATT_DOWN=line.split()[2]
	global ATT_UP
        ATT_UP=line.split()[3]

    return True
  else:
    return False

def set_led(tn,color):
  # Get xdsl info 
  tn.write("system config led "+color+"\r")
  # Wait for the prompt
  ret=tn.read_until("=>")
	
#
# main
#
# main function of the script

def main():

  #process_arg()
  try:
    tn = telnetlib.Telnet(HOST)
  except:
    print "Cannot connect to modem ("+HOST+")"
    return

  try:
    login(tn)
  except:
    print "Cannot login to modem ("+USER+")"
    return

  version(tn)

  if check_DSL(tn):
	  set_led(tn,"green")
	  print "[" + CONNECTION_TYPE + "] " + CONNECTION_BANDWIDTH
	  print "dB : " + ATT_DOWN + "/" + ATT_UP
  else:
	  set_led(tn,"red")
	  print CONNECTION_STATE


  close_connection(tn)

# this script can be used as a module for your own script, of for writing some tests ;)
# so check if this script is called directly, then calls main function
if __name__ == "__main__":
  main()
