import time
import matplotlib.pyplot as plt
import numpy as np

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
clientID=sim.simxStart(  '127.0.0.1'  ,19997,True,True,5000,5) # Connect to CoppeliaSim  '10.1.3.216'   '127.0.0.1'\


t = np.arange(0, 4*np.pi, 0.1)   # start,stop,step 0, 4*np.pi, 0.1
lenght_t = len(t)
r_hip =  25*np.cos(t)
r_knee = 45*np.cos(t)+45
l_hip =  -25*np.cos(t)
l_knee = -45*np.cos(t)+45


# plt.plot(t, r_hip, t, r_knee)
# plt.show()

if clientID!=-1:
    print ('Connected to remote API server')
    # 1. First send a command to display a specific message in a dialog box:
    emptyBuff = bytearray()

    i=0
    while i<1000:
        i += 1
        idx = i % lenght_t
        print(i)
        res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID,'Waist_respondable',sim.sim_scripttype_childscript,'setAngles',[],[r_hip[idx], l_hip[idx], r_knee[idx], l_knee[idx]],[], bytearray(),sim.simx_opmode_oneshot)
        time.sleep(100/1000)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')

