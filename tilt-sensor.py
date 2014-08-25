"""
Python HID interface for tilt-sensor (Windows only)
logs data from the sensor to file in json format
N. Seymour-Smith 24/08/14
"""
import sys
import pywinusb.hid as hid 
import time
import settings
import os
import json
from msvcrt import kbhit

def data_handler(data):
    if settings.DEBUG:
        print ("data: %s" % data[:6])
    angle = int(data[3:6])/1000

#HID request message
buffer = [0x00]*65
buffer[0]=0x0 #Endpoint
buffer[0]=0x0 #0x00 - Read, 0x01 - Write (0x02 is response code)
buffer[2]=0x5 #parameter identifier (0x05: single-axis angle)

#
device = hid.find_all_hid_devices()[0]
if not device:
    print("Can't find HID device!")
else:
    try:
        device.open()
        device.set_raw_data_handler(data_handler)
        report = device.find_output_reports()[0]
        while not kbhit():
            report.send(buffer)
            open(settings.OUTPUT_FILE, 'wb').write(
                 json.dumps([{"angle": angle}]))
            os.rename(settings.OUTPUT_FILE + ".temp", 
                      settings.OUTPUT_FILE)
            if not settings.SILENT:
                print "\nSensor angle: " + str(angle)
            time.sleep(settings.RATE)
    finally:
        device.close()
