"""
Python HID interface for tilt-sensor (Windows only)
logs data from the sensor to file in json format
N. Seymour-Smith 24/08/14
"""
 
import time
import settings
import os
import json


def record():
    running = 1
    print ("Writing sensor data to %s. \"Ctrl-C\" to quit" 
           % settings.OUTPUT_FILE)
    while running:
        try:
            angle = get_angle()
            open(settings.OUTPUT_FILE + ".temp", "wb").write(
                json.dumps([{"angle": angle}]))
            os.rename(settings.OUTPUT_FILE + ".temp", 
                      settings.OUTPUT_FILE)

            if not settings.SILENT:
                print "\nSensor angle: " + angle
            time.sleep(settings.RATE)

        except (KeyboardInterrupt, SystemExit):
            running = 0

def get_angle():
    return 0
