#!/usr/bin/python

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
# main
#

def main():

  #process_arg()

  # Telnet initialization
  tn = telnetlib.Telnet(HOST)

  # Credentials
  tn.read_until("Username : ")
  tn.write(USER + "\r")
  tn.read_until("Password : ")
  tn.write(PASSWORD + "\r")

  # Wait for the prompt
  tn.read_until("=>")

  # Get xdsl info 
  tn.write("xdsl info\r")

  # Wait for the prompt
  print tn.read_until("=>")

  # Quitting
  tn.write("exit\r")
  tn.read_all()


if __name__ == "__main__":
  main()
