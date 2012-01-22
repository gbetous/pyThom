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
# Global definition
#
# Customise for your needs
#
HOST = "192.168.0.254"
USER = "Administrator"
PASSWORD = ""

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
# xdsl_info
#
# gets and processes xdsl_info 
#
def xdsl_info(tn):
  # Get xdsl info 
  tn.write("xdsl info\r")

  # Wait for the prompt
  ret=tn.read_until("=>")

  print ret

#
# main
#
# main function of the script

def main():

  #process_arg()

  # Telnet initialization
  tn = telnetlib.Telnet(HOST)

  login(tn)

  xdsl_info(tn)

  # Quitting
  tn.write("exit\r")
  tn.read_all()

# this script can be used as a module for your own needs
# so check if this script is called directly, then calls main function
if __name__ == "__main__":
  main()
