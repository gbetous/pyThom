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
  tn.read_until("Username : ")
  tn.write(USER + "\r")
  tn.read_until("Password : ")
  tn.write(PASSWORD + "\r")

  # Wait for the prompt
  tn.read_until("=>")

#
# close_connection
#
# closes conection 
#
def close_connection(tn):
  # Quitting
  tn.write("exit\r")
  tn.read_all()


#
# xdsl_info
#
# gets and processes xdsl_info 
#
def xdsl_info(tn):
  # Get xdsl info 
  tn.write("xdsl info\r")

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

#
# status
#
# print final status
#
def status():
  if CONNECTION_STATE == "up":
    print "[" + CONNECTION_TYPE + "] " + CONNECTION_BANDWIDTH
  else:
    print CONNECTION_STATE

#
# main
#
# main function of the script

def main():

  #process_arg()

  tn = telnetlib.Telnet(HOST)

  login(tn)
  xdsl_info(tn)
 
  status()

  close_connection(tn)

# this script can be used as a module for your own script, of for writing some tests ;)
# so check if this script is called directly, then calls main function
if __name__ == "__main__":
  main()
