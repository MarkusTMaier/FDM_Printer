#!/usr/bin/env python3

import time
from sem6000_library import SEMSocket
import bluepy


PW = "0000"
MYMAC = '6C:79:B8:60:5F:9D'  #MAC adress of the Voltcraft SEM6000 device, Raspberry Pi MAC: E4:5F:01:80:F2:2E
socket = None
wattage_power = float(8.111)
while True:
  time.sleep(1)
  try:
    if socket == None:
      print("Connecting... ", end="")
      socket = SEMSocket(MYMAC)
      print("Success!")
      print("You're now connected to: {} (Icon: {})".format(socket.name, socket.icons[0]))
      if socket.login(PW) and socket.authenticated:
        print("Login successful!")
        socket.getSynConfig()
    socket.getStatus()
    #print("=== {} ({}) ===".format(socket.mac_address, "on" if socket.powered else "off"))
    #print("\t{}V {}A ? {}W@{}Hz (PF: {})".format(socket.voltage, socket.current, socket.power, socket.frequency, socket.power_factor)).
    #print("{}W".format(socket.power))
    wattage_power = socket.power
  except (SEMSocket.NotConnectedException, bluepy.btle.BTLEDisconnectError, BrokenPipeError):
    print("Restarting...")
    if socket != None:
      socket.disconnect()
      socket = None