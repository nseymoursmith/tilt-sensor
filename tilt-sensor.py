"""
Python HID interface for tilt-sensor (Windows only)
logs data from the sensor to file in json format
N. Seymour-Smith 24/08/14
"""
import sys
import pywinusb.hid as hid 
import time
import settings
import json
import struct
import shutil
import MySQLdb
from msvcrt import kbhit

def getSignedNumber(number, bitLength):
    mask = (2 ** bitLength) - 1
    if number & (1 << (bitLength - 1)):
        return number | ~mask
    else:
        return number & mask

def data_handler(data):
    bytes = data[3:7]
    angle = 0
    for i in range(4):
        temp = bytes[3-i] << 8*i
        angle += temp
    angle = getSignedNumber(angle, 32)
    angle /= 1000
    angle -= settings.OFFSET
    for i in range(len(settings.RANGES)):
        if angle < settings.RANGES[i]:
            output = i+1
            break
        else:
            output = 4
    open(settings.OUTPUT_FILE + ".temp", 'wb').write(
        json.dumps([{"active": output}]))
    shutil.move(settings.OUTPUT_FILE + ".temp", 
              settings.OUTPUT_FILE)

    if settings.SQL:
        cur.execute(sqlUpdate, (output, settings.COLUMN_ID))
        db.commit()

    if not settings.SILENT:
        print ("angle: %s\nregion: %s\n" % (angle, output))
        

#HID request message
buffer = [0x00]*65
buffer[0]=0x0 #Endpoint
buffer[0]=0x0 #0x00 - Read, 0x01 - Write (0x02 is response code)
buffer[2]=0x5 #parameter identifier (0x05: single-axis angle)

if settings.SQL:
    db = MySQLdb.connect(
        db = settings.DATABASE,
        host = settings.HOST,
        user = settings.USER,
        passwd = settings.PASS
    )
    cur = db.cursor()
    cur.execute("SELECT VERSION()")
    ver = cur.fetchone()
    print "Server version: ", ver[0]

    sqlUpdate = '''
    UPDATE mccglc_seebri_motiondetect
    SET active = (%s)
    WHERE id = (%s)
    '''
    sqlRead = '''
    SELECT active 
    FROM mccglc_seebri_motiondetect
    WHERE id = (%s)
    '''

device = hid.find_all_hid_devices()[0]
if not device:
    print("Can't find HID device!")
else:
    try:
        print("Writing output to:\n%s\nPress any key to quit\n" %
              settings.OUTPUT_FILE)
        device.open()
        device.set_raw_data_handler(data_handler)
        report = device.find_output_reports()[0]
        while not kbhit():
            report.send(buffer)
            time.sleep(settings.RATE)
    finally:
        device.close()
        if settings.SQL:
            cur.close()
            db.close()


