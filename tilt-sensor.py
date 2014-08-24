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

def record():
    running = 1
    print ("Writing sensor data to: \n%s. \n\"Ctrl-C\" to quit" 
           % settings.OUTPUT_FILE)
    while running:
        try:
            angle = get_angle()
            open(settings.OUTPUT_FILE, 'wb').write(
                json.dumps([{"angle": angle}]))
#            os.rename(settings.OUTPUT_FILE + ".temp", 
#                      settings.OUTPUT_FILE)

            if not settings.SILENT:
                print "\nSensor angle: " + str(angle)
            time.sleep(settings.RATE)

        except (KeyboardInterrupt, SystemExit):
            running = 0

def get_angle():
    angle = 0
    return angle

def data_handler(data):
    print ("data: %s" % data)

devices = hid.find_all_hid_devices()
usage = hid.get_full_usage_id(0xff00, 0x01)
buffer = [0x00]*65
buffer[0]=0x0 #Endpoint
buffer[0]=0x0 #0x00 - Read, 0x01 - Write (0x02 is response code)
buffer[2]=0x5 #parameter identifier

if not devices:
    print("Can't find HID device!")

else:

    device = devices[0]
    print device
    try:
        device.open()
        reports = device.find_output_reports()
        report = reports[0]
        device.set_raw_data_handler(data_handler)
#        print report.get_raw_data()
        while not kbhit():
            time.sleep(0.5)
            report.send(buffer)
    finally:
        device.close()
#record()
