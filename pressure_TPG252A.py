# ////////////////////////////////////////////////////////// //
#                                                            //
# python script to read the pressure with a                  //
# Pfeiffer Vacuum Dual Gauge TPG 252 A Controller, BTG28270  //
#                                                            //
# Last modifications: 19.02.2019 by R.Berner                 //
#                                                            //
# ////////////////////////////////////////////////////////// //

import serial
import subprocess
import time

# Define offset
offset_p1 = 0.0
offset_p2 = 0.0

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

#ser.isOpen()

#print "Resetting device"
#ser.write("RES,1")
#while ser.inWaiting():
#    print ser.readline()
#    time.sleep(0.1)

#print "Automatically enable/disable sensors 1,2"
#ser.write("SEN,2,2")
#while ser.inWaiting():
#    print ser.readline()
#    time.sleep(0.1)

#print "Set measurement unit to mbar"
#ser.write("UNI,2")
#while ser.inWaiting():
#    print ser.readline()
#    time.sleep(0.1)

#print "Set entry lock function off"
#ser.write("LOC,0")
#while ser.inWaiting():
#    print ser.readline()
#    time.sleep(0.1)

#print "Set rate to 9600 Baud"
#ser.write("BAU,4")
#while ser.inWaiting():
#    print ser.readline()
#    time.sleep(0.1)

#print "Set filter time constant to normal"
#ser.write("FIL,1,1")
#while ser.inWaiting():
#    print ser.readline()
#    time.sleep(0.1)

#print "Set calibration factor"
#ser.write("CAL,1.000,1.000")
#while ser.inWaiting():
#    print ser.readline()
#    time.sleep(0.1)

#print "Set range to 2 bar"
#ser.write("FSR,4,4")
#while ser.inWaiting():
#    print ser.readline()
#    time.sleep(0.1)

#print "Set offset correction"
#ser.write("OFC,0,0")
#while ser.inWaiting():
#    ser.readline()
#    time.sleep(0.1)

#print "Test program"
#ser.write("RST")
#while ser.inWaiting():
#    ser.readline()
#time.sleep(0.1)

#print("I\\O-test (6s)")
#ser.write("IOT\r\n")
#while ser.inWaiting():
    #ser.readline()
    #time.sleep(6)

#print("Enable continuous output mode")
#ser.write("COM")
#while ser.inWaiting():
    #ser.readline()
    #time.sleep(0.1)

ser.write("PRX")
while ser.inWaiting():
    ser.readline()
time.sleep(1)

while 1:
    ser.write("\x05\r\n") # Request for data transmission (see manual p. 5)
    while ser.inWaiting() > 0:
        answer = ser.readline()
        try:
            statusCode_p1 = int(answer.split(',')[0])
            p1 = float(answer.split(',')[1]) + offset_p1
            statusCode_p2 = int(answer.split(',')[2])
            p2 = float(answer.split(',')[3]) + offset_p2

            # Send data to database (onlz if data is of good qualitz, e.g. statusCode==0)
            if statusCode_p1==0 and p1>=0.:
                print "p1 =", p1, "mbar"
                post1_bar = "pressure_bar,sensor=1,pos=atmosphere value=" + str(p1)
                subprocess.call(["curl", "-i", "-XPOST", "lhepdaq2.unibe.ch:8086/write?db=module_zero_run_jan2019", "--data-binary", post1_bar])
            if statusCode_p1==1: print "Sensor 1: Underrange"
            if statusCode_p1==2: print "Sensor 1: Overrange"
            if statusCode_p1==3: print "Sensor 1: Sensor error"
            if statusCode_p1==4: print "Sensor 1: Sensor off"
            if statusCode_p1==5: print "Sensor 1: No sensor (output: 5,2000E-2)"
            if statusCode_p1==6: print "Sensor 1: Identification error"

            if statusCode_p2==0 and p2>=0.:
                print "p2 =", p2, "mbar"
                post2_bar = "pressure_bar,sensor=2,pos=module value=" + str(p2)
                subprocess.call(["curl", "-i", "-XPOST", "lhepdaq2.unibe.ch:8086/write?db=module_zero_run_jan2019", "--data-binary", post2_bar])
            if statusCode_p2==1: print "Sensor 2: Underrange"
            if statusCode_p2==2: print "Sensor 2: Overrange"
            if statusCode_p2==3: print "Sensor 2: Sensor error"
            if statusCode_p2==4: print "Sensor 2: Sensor off"
            if statusCode_p2==5: print "Sensor 2: No sensor (output: 5,2000E-2)"
            if statusCode_p2==6: print "Sensor 2: Identification error"

            time.sleep(1)

        except (ValueError,IndexError):
            #print "error"
            pass

        time.sleep(1)
