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
RATE_DOWN = "x"
RATE_UP = "x"
SW_VERSION = ""

def my_read_until(tn,str_until,timeout=5):
  ret=tn.read_until(str_until.encode(),timeout)
  return ret

#
# process_arg
#
# reads command line arguments and sets application configuration
#
def process_arg():
  for arg in sys.argv:
    print(arg)

#
# login
#
# sends login and password to telnet connection 
#
def login(tn):
  my_read_until(tn,"Username : ",5)
  tn.write((USER + "\r").encode())
  my_read_until(tn,"Password : ",5)
  tn.write((PASSWORD + "\r").encode())
  # Wait for the prompt
  try:
    my_read_until(tn,"=>")
  except:
    print("Could not connect to modem ("+USER+")")

#
# close_connection
#
# closes conection 
#
def config_dump(tn):
  tn.write(b"config dump user.ini\r")
  ret=my_read_until(tn,"=>")

  f = open('pyThom.ini', 'w')

  for l in ret.splitlines():
    line=str(l,encoding="utf8")
    if "=>" not in line and "config dump" not in line:
      f.write(line+"\n")
  f.close()

def close_connection(tn):
  # Quitting
  tn.write(b"exit\r")
  tn.read_all()

def version(tn):
   # Get xdsl info 
  tn.write(b"software version\r")
  # Wait for the prompt
  ret=my_read_until(tn,"=>")

  for l in ret.splitlines():
    line=str(l,encoding='utf8')
    if "Active" in line:
      SW_VERSION=line.split()[3]
      print(SW_VERSION)

#
# check_DSL
#
# return TRUE if connected 
#
def check_DSL(tn):

  global CONNECTION_STATE, CONNECTION_TYPE, CONNECTION_BANDWITH, ATT_DOWN, ATT_UP, RATE_DOWN, RATE_UP

  # Get xdsl info 
  tn.write(b"xdsl info \r")
  # Wait for the prompt
  ret=my_read_until(tn,"=>")

  for l in ret.splitlines():
    line=str(l,encoding='utf8')
    if "Modem state" in line:
      CONNECTION_STATE=line.split()[2]
    if "xDSL Type" in line:
      CONNECTION_TYPE=line.split()[2]
    if "Bandwidth" in line:
      CONNECTION_BANDWIDTH=line.split()[4]

  # Get more infos if connected
  if CONNECTION_STATE == "up":
    # Get xdsl info 
    tn.write(b"xdsl info expand=enabled\r")
    # Wait for the prompt
    ret=my_read_until(tn,"=>")
    for l in ret.splitlines():
      line=str(l,encoding='utf8')
      if "Attenuation" in line:
        ATT_DOWN=line.split()[2]
        ATT_UP=line.split()[3]
      if "Payload rate" in line:
        RATE_DOWN=line.split()[3]
        RATE_UP=line.split()[4]

    return True
  else:
    return False

def set_led(tn,color):
  # Get xdsl info 
  tn.write(b"system config led "+color.encode()+b"\r")
  # Wait for the prompt
  ret=my_read_until(tn,"=>")
	
#
# main
#
# main function of the script

def main():

  #process_arg()
  try:
    tn = telnetlib.Telnet(HOST,23,5)
  except:
    print("Cannot connect to modem ("+HOST+")")
    return

  try:
    login(tn)
  except:
    print("Cannot login to modem ("+USER+")")
    return

  version(tn)
  config_dump(tn)

  if check_DSL(tn):
	  set_led(tn,"green")
	  print("[" + CONNECTION_TYPE + "] " + CONNECTION_BANDWIDTH)
	  print("dB : " + ATT_DOWN + "/" + ATT_UP)
	  print("kbps : " + RATE_DOWN + "/" + RATE_UP)
  else:
	  set_led(tn,"red")
	  print(CONNECTION_STATE)


  close_connection(tn)

# this script can be used as a module for your own script, of for writing some tests ;)
# so check if this script is called directly, then calls main function
if __name__ == "__main__":
  main()
