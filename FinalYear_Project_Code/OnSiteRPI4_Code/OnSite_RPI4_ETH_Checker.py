# Programmer: Jonathan Logue
# Date: 17/3/2021
# Project: Sligo IT Final Year project - CHLORINE DISINFECTION SYSTEM DATA ANALYSIS & CONTROL
#
# Code Description: Code is built to monitor the pyModbus connection status, when the connection is ok
# the connection_status = true & when the connection has failed the connection status = false 
# this code monitors that status & prints a 0 = false or 1 = true to the database to be then picked up by the 
# static_alarm code to trigger SMS alarms for this condition

# Import Librarys
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient
from firebase import firebase

# Assign the firebase reference. 
firebase = firebase.FirebaseApplication('https://data-793f6-default-rtdb.firebaseio.com/',None)

#Defines the client PLC's IP address for communications
IP = '10.36.35.240'

while True:
    
	#create client using the IP address
    client = ModbusTcpClient(IP)
    #check client connection & store it in connection_status
    connection_status = client.connect()
    #connection_status = 'test'
    # Print results to console
    print('---------------Comms Status--------------')
    print('Communication Status with PLC:',connection_status)
    print('---------------Comms Status--------------\n')

    #Check if status is good, if so, push '1' to database.
    if connection_status == 1:
    	comms1 = firebase.put('/Z_DEBUG - SYS Admin use only/Site_Device_Stats/','ETHERNET LAN STATUS',1) #update data
    else:
    	#if not then push a '0' to the database.
    	comms1 = firebase.put('/Z_DEBUG - SYS Admin use only/Site_Device_Stats/','ETHERNET LAN STATUS',0) #update data 

    	

    


