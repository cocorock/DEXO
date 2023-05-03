import serial
import time
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
port = 'COM8'
# Set the baud rate (e.g., 9600)
baud_rate = 115200

# Open the serial port
ser = serial.Serial(
    port=port,\
    baudrate=baud_rate,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

# Allow some time for the serial port to initialize
print ('Wait (2s)')
time.sleep(2)

sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart(  '127.0.0.1' ,19997,True,True,5000,5) # Connect to CoppeliaSim  '10.1.3.216'   '127.0.0.1'


try:
    if clientID!=-1:
        print ('Connected to remote API server')
        emptyBuff = bytearray()
        flag=0
        out=''
        # print('1')
        ser.inWaiting()
        for i in range(3):
            print(i, end='\r')
            time.sleep(1)
        ser.flush()

    while True:
        # Read a line from the serial port
        line = ser.readline().decode('utf-8')
        #print("Input: ", end='')
        #print(line, end='')
    
        # Strip the newline character and split the line by commas
        tokens = line.strip().split(',')
        # Check if there are > 4 tokens
        if len(tokens) > 4:
            tokens = tokens[0:4]
        # Check if there are 4 tokens
        #print(tokens, end='\t')
        if len(tokens) == 4:
            try:
                #print ('5', end='\t')
                # Convert the tokens to float and assign them to a, b, c, and d
                r_hip, l_hip, r_knee, l_knee = [float(token) for token in tokens]   
                # Print the received values
                #print ('Out: ', end='')
                print(f"r_hip: {r_hip:.2f}, l_hip: {l_hip:.2f}, r_knee: {r_knee:.2f}, l_knee: {l_knee:.2f}" )

                res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID,'Waist_respondable',sim.sim_scripttype_childscript,'setAngles',[],[r_hip,-l_hip,-r_knee,l_knee],[], bytearray(),sim.simx_opmode_oneshot)

            except ValueError:
                print("Error: Invalid data format")
        else: 
            print("\n>len "+str(len(tokens)), end='\t')
            print(tokens)
            ser.flush()

        time.sleep(200/1000)

except KeyboardInterrupt:
    # Close the serial port when the user presses Ctrl+C
    ser.close()