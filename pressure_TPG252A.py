# ////////////////////////////////////////////////////////// //
#                                                            //
# python script to read the pressure with a                  //
# Pfeiffer Vacuum Dual Gauge TPG 252 A Controller, BTG28270  //
#                                                            //
# Last modifications: 12.01.2019 by R.Berner                 //
#                                                            //
# ////////////////////////////////////////////////////////// //

import serial
import subprocess
import time

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

while ser.inWaiting() > 0:
    ser.readline()

ser.isOpen()

print("Resetting device")
ser.write("RES\r\n")
time.sleep(1)
ser.readline()

#print("I\\O-test (6s) ... ")
#ser.write("IOT\r\n")
#time.sleep(6)
#ser.readline()

print("Enable sensor 1")
ser.write("SEN,1,2\r\n")
time.sleep(1)
ser.readline()

print("Enable continuous output mode")
ser.write("COM\r\n")
time.sleep(1)
ser.readline()

print("Access sensor 1")
ser.write("PR1\r\n")
time.sleep(1)

while ser.inWaiting() > 0:
    ser.readline()

while 1:
    ser.write("\x05\r\n")
    time.sleep(1)
    while ser.inWaiting() > 9:
        value = ser.readline()[2:10]
        if value < 0.:
            value = 0.
        print value
        post_bar = "pressure_bar,sensor=1,pos=module value=" + str(value)
        subprocess.call(["curl", "-i", "-XPOST", "lhepdaq2.unibe.ch:8086/write?db=module_zero_run_jan2019", "--data-binary", post_bar])
