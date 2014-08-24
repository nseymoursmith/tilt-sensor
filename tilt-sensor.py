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



if not devices:
    print("Can't find HID device!")

else:

    device = devices[0]
    print device
    for attr in dir(device):
        print attr
    print "-------------------"
    
    try:
        device.open()
        for report in device.find_output_reports():
            print report
            for attr in dir(report):
                print attr
            print report.get_usages()
            usage_key = report.get_usages().keys()[0]
            print usage_key
            report[usage_key] = "0" 
            report.send()
#            report.set_raw_data(message)
        print "-----------------"
        device.set_raw_data_handler(data_handler)
# 
# device.send_output_report((0x00,0x00))
    finally:
        device.close()
#record()
