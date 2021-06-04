# Programmer: Jonathan Logue
# Date: 17/3/2021
# Project: Sligo IT Final Year project - CHLORINE DISINFECTION SYSTEM DATA ANALYSIS & CONTROL
#
# Code Description: This code handles some of the condition monitoring as well as some of the GPIO triggers
# to the SMS system to call for the SMS functions. This code handles the heartbeat monitoring of the on-site
# RPI4. the code counts 3 variables, how many times the loop catches a frozen 0 or a frozen 1
# if the heartbeat has toggled by the next cycle this is considered an RTU_OK contition,
# these are also counted.
# if 30 frozen 0's or frozen 1's are reached before 10 RTU_OK's then the heartbeat if considered to be frozen
# at this point the Loss of heartbeat trigger is sent to the arduino.
# if 10 RTU_OK's are reached before the frozen bits hit 30 the counts are reset to 0 as the heartbeat is considered ok
# code then sleeps for an hour before checking heartbeat again.


# Importing librarys
from gpiozero import LED
import threading
from firebase import firebase
firebase = firebase.FirebaseApplication('https://data-793f6-default-rtdb.firebaseio.com/',None)
from time import sleep
import time

# Assigning GPIO to SMS's 
Hb_Error_GPIO = LED(23)
ML_Error_GPIO = LED(17)
mig_Error_GPIO = LED(27)
Chl_Hi_GPIO = LED(22)

# Initialising counts
RTU_OK = 0 
frozen_zero = 0
frozen_ones = 0
hBLoss_SMS_count = 0

# Creating strings for testing stats to be sent to the database
locked = 'LOCKED'
unlocked = 'UNLOCKED'
running = 'RUNNING'

# Loop forever
while True:

    # Pull the on-site RPI4 heartbeat from the cloud database
    heartbeat = firebase.get('SITE_Pi_STATUS/Heartbeat_RTU','')

    # While the heartbeat is a 0 enter loop
    while heartbeat == 0:
        # Initialise ocount
        ocount=1
        # Enter counter up to 1325 (13secs)
        while ocount <= 1325:
            print('0 check in progress - ',ocount)
            ocount += 1
        # Check if heartbeat has toggled after time delay    
        heartbeat = firebase.get('SITE_Pi_STATUS/Heartbeat_RTU','') 
        # if it has, then RTU is consider ok, add to the RTU_OK count
        if heartbeat == 1:
            print('RTU OK')
            RTU_OK = RTU_OK + 1
        else:
            #if after time delay the heartbeat is still 0 then, add to the frozen 0 count
            print('frozen 0')
            frozen_zero = frozen_zero + 1
            break
            
    # While the heartbeat is a 0 enter loop
    while heartbeat == 1:
        # Initialise icount
        icount=1
        # Enter counter up to 1325 (13secs)
        while icount <= 1325:
            print('1 check in progress - ',icount)
            icount += 1
        # Check if heartbeat has toggled after time delay     
        heartbeat = firebase.get('SITE_Pi_STATUS/Heartbeat_RTU','')    
        # If it has, then RTU is consider ok, add to the RTU_OK count
        if heartbeat == 0:
            print('RTU OK')
            RTU_OK = RTU_OK + 1
        else:
            #If after time delay the heartbeat is still 0 then, add to the frozen 0 count
            print('frozen 1')
            frozen_ones = frozen_ones + 1
            break
    # Print Stats to console & database.        
    print('------STATUS MSG--------')
    print('RTU_Ok pings: ',RTU_OK)
    print('Frozen 0 pings: ',frozen_zero)
    print('Frozen 1 pings: ',frozen_ones)
    db = firebase.put('Z_DEBUG - SYS Admin use only/Site_Device_Stats','RTU_OK_COUNT',RTU_OK)
    db = firebase.put('Z_DEBUG - SYS Admin use only/Site_Device_Stats','FROZEN_0_COUNT',frozen_zero)
    db = firebase.put('Z_DEBUG - SYS Admin use only/Site_Device_Stats','FROZEN_1_COUNT',frozen_ones)

    # If RTU_OK gets past 10, heartbeat considered ok so reset the counts
    if RTU_OK > 10:
        print('Resetting counts')
        RTU_OK = 0
        frozen_zero = 0
        frozen_ones = 0
    # If either the frozen 0 or frozen 1 counts exceed 30 then heartbeat considered frozen, trigger sent to ardunio  
    if frozen_zero > 30 or frozen_ones > 30:
        # Count stats 
        hBLoss_SMS_count = hBLoss_SMS_count + 1
        # Push stats to database
        db = firebase.put('Z_DEBUG - SYS Admin use only/Site_Device_Stats','Program status (locked for timeframe after SMS sent)',locked)
        db = firebase.put('/OFFICE_Pi_STATUS/','Heartbeat_Monitoring_Code_Status',locked)
        # Set GPIO to high
        Hb_Error_GPIO.toggle()
        sleep(5)
        # Turn GPIO off
        Hb_Error_GPIO.off()
        # Reset counts
        frozen_zero = 0
        frozen_ones = 0
    # Print stats    
    db = firebase.put('Z_DEBUG - SYS Admin use only/SMS_Stats','Loss of Heartbeat SMS sent',hBLoss_SMS_count)
    db = firebase.put('Z_DEBUG - SYS Admin use only/Site_Device_Stats','Program status (locked for timeframe after SMS sent)',unlocked)
    db = firebase.put('/OFFICE_Pi_STATUS/','Heartbeat_Monitoring_Code_Status',running)
    sleep(3600)

    
        
  



    
 
