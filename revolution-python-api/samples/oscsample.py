import time
import argparse
import random

from bitalino import BITalino
from pythonosc import osc_message_builder
from pythonosc import udp_client

# The macAddress variable on Windows can be "XX:XX:XX:XX:XX:XX" or "COMX"
# while on Mac OS can be "/dev/tty.BITalino-XX-XX-DevB" for devices ending with the last 4 digits of the MAC address or "/dev/tty.BITalino-DevB" for the remaining
# macAddress = "/dev/tty.BITalino-C8-28-DevB"
# macAddress = "/dev/tty.BITalino-DevB"
# macAddress = "46:61:B6:9D:F4:05" # Bitalino BLE 1
macAddress = "84:BA:20:AE:B6:01" # Bitalino BLE 2
# macAddress = "20:16:04:12:00:48" # Bitalino Bluetooth 'old'
 

# OSC Settings
sendToAddress           = "192.168.0.242" #ip adress of the client
sendToPort              = 5005

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default=sendToAddress,
	  help="The ip of the OSC server")
 
  parser.add_argument("--port", type=int, default=5005,
	  help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)



# This example will collect data for 5 sec.
running_time = 5000

batteryThreshold = 0
acqChannels = [0, 1, 2, 3, 4, 5]
samplingRate = 100
nSamples = 10

digitalOutput_on = [1, 1]
digitalOutput_off = [0, 0]

# Connect to BITalino
device = BITalino(macAddress)


# Set battery threshold
device.battery(batteryThreshold)

# Read BITalino version
print(device.version())

# Start Acquisition
device.start(samplingRate, acqChannels)

start = time.time()
end = time.time()
while (end - start) < running_time:
    # Read samples
    
    for x in device.read(nSamples):

      print(x)
    
      channel1 = x[5]
      channel2 = x[6]
      channel3 = x[7]
      channel4 = x[8]
      channel5 = x[9]
      channel6 = x[10]

      # send chanels via OSC
      client.send_message("/a1", float(channel1))
      client.send_message("/a2", float(channel2))
      client.send_message("/a3", float(channel3))
      client.send_message("/a4", float(channel4))
      client.send_message("/a5", float(channel5))
      client.send_message("/a6", float(channel6))


    # channel8 = device.read(nSamples)[0][7]
    # channel9 = device.read(nSamples)[0][8]

    # print(channel6)
    # print(channel7)


    # client.send_message("/channel8", float(channel8))
    # client.send_message("/channel9", float(channel9))

    end = time.time()

# Turn BITalino led and buzzer on
device.trigger(digitalOutput_on)
# Script sleeps for n seconds
time.sleep(running_time)

# Turn BITalino led and buzzer off
device.trigger(digitalOutput_off)

# Stop acquisition
device.stop()

# Close connection
device.close()
