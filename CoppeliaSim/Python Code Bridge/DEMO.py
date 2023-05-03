import serial
import time

ser = serial.Serial(
    port='COM12',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print ('Wait (2s)')
time.sleep(2)
try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import sys
import ctypes
print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart(  '127.0.0.1' ,19997,True,True,5000,5) # Connect to CoppeliaSim  '10.1.3.216'   '127.0.0.1'

try:
    if clientID!=-1:
        print ('Connected to remote API server')
        # 1. First send a command to display a specific message in a dialog box:
        emptyBuff = bytearray()
        #res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID,'remoteApiCommandServer',sim.sim_scripttype_childscript,'displayText_function',[],[],['Hello world!'],emptyBuff,sim.simx_opmode_blocking)
        flag=0
        out=''
        # print('1')
        ser.inWaiting()
        for i in range(3):
            print(i, end='\r')
            time.sleep(1)
        ser.flush()
        # while flag!= 1 :
        #     #print('2')
        #     while (ser.inWaiting() > 0):
        #         out = str(ser.readline(), "utf-8")
        #         print('-> '+out)
        #         #print('3')

        #     if (out == str('IN!\r\n')):
        #         print(str('------------------>>>> IN! <<<<----------------------'))
        #         flag =1
        #     time.sleep(3/1000)
            
        out=''
        i=0
        r_hip=0
        l_hip=0
        r_knee=0
        l_knee=0
        while i<1000:
            i=1+i
            print('i'+str(i)+'\t', end='')
            while ser.inWaiting() > 0:
                out = str(ser.readline(), "utf-8")
                # print('>>'+ out)
            str1 = out.split(',')
            L = len(str1)
            #print('len '+ str(L))
            if L==4:
                a,b,c,d= out.split(',')
                r_hip = int(a)
                l_hip = int(b)
                r_knee = int(c)
                l_knee = int(d)
                #print('weeee\t', end='')
                print(str(a)+'\t'+str(b)+'\t'+str(c))
            else:
                print('len: '+str(L))
            # try:
            #     piece = str1.index(1)
            #     if (piece != '\r\n'):
            #         r_hip = int(str1.pop())
            #         #l_hip = int(str1.pop())
            #         #r_knee = int(str1.pop())
            #         print('==='+str(r_hip+'\t'+l_hip+'\t'+r_knee))
            # except:
            #     print ('..') 

            
            res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID,'Waist_respondable',sim.sim_scripttype_childscript,'setAngles',[],[r_hip,-l_hip,-r_knee,l_knee],[], bytearray(),sim.simx_opmode_oneshot)
            ser.flush()
            time.sleep(200/1000)
        ser.close()

        

        # Now close the connection to CoppeliaSim:
        sim.simxFinish(clientID)
    else:
        print ('Failed connecting to remote API server')
    print ('Program ended')
except KeyboardInterrupt:
    # Close the serial port when the user presses Ctrl+C
    ser.close()