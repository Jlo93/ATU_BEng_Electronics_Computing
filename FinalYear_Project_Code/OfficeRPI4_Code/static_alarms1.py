# Programmer: Jonathan Logue
# Date: 17/3/2021
# Project: Sligo IT Final Year project - CHLORINE DISINFECTION SYSTEM DATA ANALYSIS & CONTROL
#
# Code Description: This code handles some of the more static alarm conditions that then trigger the
# GPIO pins to signal to the Arduino to enter the specific SMS functions and delivery the messages.
# it pulls the data into the program from the cloud and monitors the values coming in for the following
# conditions, Hi chlorine SP & chlorine reading, the ML ref SP & the actual ML output as well as calculating
# the percentage error between the two & the data migration if loss of LAN connection between the PLC & RPI4.

# Importing librarys
from gpiozero import LED
import threading
from firebase import firebase
firebase = firebase.FirebaseApplication('https://data-793f6-default-rtdb.firebaseio.com/',None)
from time import sleep
import time


# Assigning GPIO to SMS's 
ML_Error_GPIO = LED(17)
mig_Error_GPIO = LED(27)
Chl_Hi_GPIO = LED(22)

# Initialising counts
ML_SMS_count = 0
dataMig_SMS_count = 0
ChlHi_SMS_count = 0
unlocked = 'UNLOCKED'
running = 'RUNNING'


while True:
    
    # Pull in the relevant data required from the cloud database. 
    Cl_Hi = firebase.get('Data/ML Data & SMS Alarm Setpoints/Chlorine (CL001) High SP','')
    CL001 = firebase.get('Data/Process Variables (ML Model Inputs)/Cl Res CL001','')
    MlAnomolyRef = firebase.get('Data/ML Data & SMS Alarm Setpoints/ML Anomoly Reference SP','')
    MlOutput = firebase.get('Data/ML Data & SMS Alarm Setpoints/ML Suggested Control Set-Point (ML Model Output)','')
    EthStatus = firebase.get('Z_DEBUG - SYS Admin use only/Site_Device_Stats/ETHERNET LAN STATUS','')
    #print(Cl_Hi)
    #print(CL001)
    #print(MlAnomolyRef)
    #print(MlOutput)
    print(EthStatus)
    
    #calculate the percenatge error between the ML output & the ML refrence SP.
    percError = (((MlAnomolyRef-MlOutput)/MlOutput)*100)
    #print(percError)

    # If the percError is less than 0, i.e a minus number depending on weather the SP is above or below the ML output.
    if percError < 0:
        # Drop the negative by making the number an absolute.
        percError = abs(percError)
        #print('Percentage Error between Model Output & Reference SP is: %',percError)

        # Push the calculated percengtage error to the cloud.
        pError = firebase.put('/Data/ML Data & SMS Alarm Setpoints/','ML Suggested SP and Ref SP percentage Error',percError)
    else:
        #print('Percentage Error between Model Output & Reference SP is: %',percError)
        pError = firebase.put('/Data/ML Data & SMS Alarm Setpoints/','ML Suggested SP and Ref SP percentage Error',percError)    
    
    # If the chlorine residual value is greater than the Chlorine High setpoint the trigger is sent to the ardunio SMS system
    if CL001 > Cl_Hi:
        # Add to the SMS count
        ChlHi_SMS_count = ChlHi_SMS_count + 1
        # Toggle the GPIO
        Chl_Hi_GPIO.toggle()
        sleep(5)
        # Turn the GPIO off
        Chl_Hi_GPIO.off()
        sleep(60)

    # If the percentage error is outside of the +/-5% tolerance then the trigger is sent to the SMS system. 
    if percError > 5:
        # Add to the SMS count
        ML_SMS_count = ML_SMS_count + 1
        # Toggle the GPIO
        ML_Error_GPIO.toggle()
        sleep(5)
        # Turn the GPIO off
        ML_Error_GPIO.off()
        sleep(60)

    # If the EthStatus is equal to 0 this is an indication that the LAN has been disconnected, trigger is sent to the SMS system
    if EthStatus == 0:

        print(EthStatus)
        # Add to the SMS count
        print('im in here')
        dataMig_SMS_count = dataMig_SMS_count + 1
        # Toggle the GPIO
        mig_Error_GPIO.toggle()
        sleep(5)
        # Turn the GPIO off
        mig_Error_GPIO.off()
        sleep(60)
        
    # Push SMS stats to the database     
    db = firebase.put('Z_DEBUG - SYS Admin use only/SMS_Stats','ML output anomoly SMS sent total',ML_SMS_count)
    db = firebase.put('Z_DEBUG - SYS Admin use only/SMS_Stats','Chlorine high alarm SMS total',ChlHi_SMS_count)
    db = firebase.put('Z_DEBUG - SYS Admin use only/SMS_Stats','Data migration failed SMS total',dataMig_SMS_count)
    db = firebase.put('/OFFICE_Pi_STATUS/','Static_Alarms_Code_Status',running)
        
             

        
    
