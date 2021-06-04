# Programmer: Jonathan Logue
# Date: 3/3/2021
# Project: Sligo IT Final Year project - CHLORINE DISINFECTION SYSTEM DATA ANALYSIS & CONTROL
#
# Code Description: This code is running on the On-Site RPI4 & it has various critical functions.
#              
# Function 1 - PLC_Tasks: 
#              Function Inputs - Target device IP address, Target memory word, data length to pull
#              Returns - Float value of the desired data stored on target memory word
#              Description: 
#              This function uses the pyModbus library to make a connection between the RPI4
#              and the PLC via Ethernet having had the target device IP address passed to the function.
#              The function then reads the data from the PLC holding register(Memory Word) also passed 
#              to the function along with the data length we require in this case '2' (2 Bytes).
#              The value which is initially a hex value is then packed into a struct(structure), 
#              before the fucntion unpacks the byte(byte 0) we need in a float data type.
#              This float value is then returned out into the main program. 
#
#Function 2 - Data_Generator: 
#              Function Inputs - No Inputs
#              Returns - Randomised floating point data tags.
#              Description: 
#              This function was created to aid in the build phase of the project, to allow for debugging &
#              testing of various functions before a live stream of 'real' data could be fed to the program.
#              The code generates random data which is limited between a range (Lower & Higher range) by using 
#              the random .uniform() function. this allowed me to simulate for example a 'live' stream of changing
#              data for example a flow meter value varying around 10-20m3/hr or a temperature value flucuating between 
#              8.5-12.3 degrees. 
#
#Function 3 - show_input_data: 
#              Function Inputs - No Inputs
#              Returns - a print of the data tags.
#              Description:
#              This function was also created for testing & debugging it, was used to give me a visual that the data
#              tags being fed to the ML model or to the cloud had values assigned to them either from random generation
#              via the Data_Generator function or from live data reading via PLC_Tasks function.
#
#Function 4 - Database_Update: 
#              Function Inputs - Data tags, process variables read from the PLC & 1 control setpoint suggestion
#              outputted from the model.
#              Returns - No returns from the function to this program
#              Description:
#              This function is used to write our data to the cloud database, inside the fucntion i have included the 
#              databse address(child) where the data is to be written along with its assigned data tag passed into the
#              function, i am writing to my firebase database using the firebase.put() function which is defined in the
#              firebase docs as 'Write or replace data to a defined path, like messages/users/user1/<data>'
#
#
#
# 

#Importing Libraries
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import struct
import pymodbus
import threading
import time
import random 
import warnings
warnings.filterwarnings("ignore")
from firebase import firebase
from sklearn import neighbors,datasets
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import metrics
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient

#Assigning the firebase address reference
firebase = firebase.FirebaseApplication('https://data-793f6-default-rtdb.firebaseio.com/',None)

# Defines the client PLC's IP address for communications
IP = '10.36.35.240'

# Function Establishes connection and checks comms status
def PLC_Tasks(IP_Address,memory_Word,data_Length):

	client = ModbusTcpClient(IP_Address)
	connection_status = client.connect()
	#print('---------------Comms Status--------------')
	#print('Communication Status with PLC:',connection_status)
	#print('---------------Comms Status--------------\n')
	#comms1 = firebase.put('/Z_DEBUG - SYS Admin use only/Site_Device_Stats/','ETHERNET LAN STATUS',connection_status) #update data

	rr = client.read_holding_registers(memory_Word,data_Length) #>rr = client.read_holdiing_registers(5524,2)< worked last test
	#Sets up the decoder to decode the chosen memory word, endian is set to big as the M340 byte order has to be swapped on decoding
	decoder = BinaryPayloadDecoder.fromRegisters(rr.registers, Endian.Big, wordorder=Endian.Big)
	initialVal = decoder.decode_32bit_float()
	raw = struct.pack('>HH',rr.getRegister(1),rr.getRegister(0))
	value = struct.unpack('>f',raw)[0]

	#print(value)
	return value

# Function to generate instrumentation data for testing live algorithim & database handling.
def data_generator():

	CL001 = random.uniform(1.4,1.65)
	CL002 = random.uniform(1.3,1.5)
	ph001 = random.uniform(10.5,8.4)
	TP001 = random.uniform(11.5,11.9)
	TCTEFF = random.uniform(120.0,125.0)
	FL001 = random.uniform(7.8,8.3)
	TU001 = random.uniform(0.075,0.08)
	CL_T1_VOL = random.uniform(318,320)
	FL004 = random.uniform(7.8,8.2)
	LI001 = random.uniform(0.45,0.47)
	CLDOSE = random.uniform(2.44,2.48)
	M001 = random.uniform(0.0475,0.0495)

	return (CL001,CL002,ph001,TP001,TCTEFF,FL001,TU001,CL_T1_VOL,FL004,LI001,CLDOSE,M001)

# Function to print data tags, for testing & verification    
def show_input_data():
    
    print('-------------Data Generator--------------')
    print('Simulated data <CL001> :',CL001_IP)
    print('Simulated data <CL002> :',CL002_IP)
    print('Simulated data <pH001> :',ph001_IP)
    print('Simulated data <TP001> :',TP001_IP)
    print('Simulated data <TCTEFF> :',TCTEFF_IP)
    print('Simulated data <FL001> :',FL001_IP)
    print('Simulated data <TU001> :',TU001_IP)
    print('Simulated data <CL_T1_VOL> :',CL_T1_VOL_IP)
    print('Simulated data <FL004> :',FL004_IP)
    print('Simulated data <LI001> :',LI001_IP)
    print('Simulated data <CLDOSE> :',CLDOSE_IP)
    print('Simulated data <M001> :',M001_IP)
    print('-------------Data Generator--------------')

# Function to continuously update the real-time data base values.
def Database_Update(tcteff,ph001,tp001,cl001,cl002,Cltar_Pred,tu001,fl001,fl004,li001):
	#threading.Timer(0.50, Database_Update).start()

	result = firebase.put('/Data/Process Variables (ML Model Inputs)/','Contact Time(TCTEFF)',tcteff) #update data
	result = firebase.put('/Data/Process Variables (ML Model Inputs)/','pH',ph001)
	result = firebase.put('/Data/Process Variables (ML Model Inputs)/','Temp',tp001) #update data
	result = firebase.put('/Data/Process Variables (ML Model Inputs)/','Cl Res CL001',cl001) #update data
	result = firebase.put('/Data/Process Variables (ML Model Inputs)/','Cl Val CL002',cl002) #update data
	result = firebase.put('/Data/ML Data & SMS Alarm Setpoints/','ML Suggested Control Set-Point (ML Model Output)',Cltar_Pred) #update data
	result = firebase.put('/Data/Process Variables (ML Model Inputs)/','Turbidity TU001',tu001) #update data
	result = firebase.put('/Data/Process Variables (ML Model Inputs)/','Inflow FL001',fl001) #update data
	result = firebase.put('/Data/Process Variables (ML Model Inputs)/','Outlet Flow FL004',fl004) #update data
	result = firebase.put('/Data/Process Variables (ML Model Inputs)/','Reservoir Level LI001',li001) #update data
	
# Importing the dataset via CSV file.
data = pd.read_csv("/home/pi/Desktop/MilfordData.csv", low_memory=False)

# Selecting the relevant data columns from the dataset an d creating a new dataframe to hold the relevant data
df1 = data[['CL001', 'CL002','CLTAR','pH001','TP001','CTTAR','TCTEFF','FL001','TU001','CL_T1_VOL','FL004','LI001','M001','CLDOSE',]]

# Data Cleaning & processing
# Changing the data types from objects type to numerical float type to allow to be processed through the ML model
df1['CL001'] = pd.to_numeric(df1['CL001'],errors ='coerce')
df1['CL002'] = pd.to_numeric(df1['CL002'],errors ='coerce')
df1['CLTAR'] = pd.to_numeric(df1['CLTAR'],errors ='coerce')
df1['pH001'] = pd.to_numeric(df1['pH001'],errors ='coerce')
df1['TP001'] = pd.to_numeric(df1['TP001'],errors ='coerce')
df1['CTTAR'] = pd.to_numeric(df1['CTTAR'],errors ='coerce')
df1['TCTEFF'] = pd.to_numeric(df1['TCTEFF'],errors ='coerce')
df1['FL001'] = pd.to_numeric(df1['FL001'],errors ='coerce')
df1['TU001'] = pd.to_numeric(df1['TU001'],errors ='coerce')
df1['CLDOSE'] = pd.to_numeric(df1['CLDOSE'],errors ='coerce')
df1['CL_T1_VOL'] = pd.to_numeric(df1['CL_T1_VOL'],errors ='coerce')
df1['FL004'] = pd.to_numeric(df1['FL004'],errors ='coerce')
df1['LI001'] = pd.to_numeric(df1['LI001'],errors ='coerce')

# function to sift through entire dataframe and drop any labels with NaN
# Any labels with NaN will cause errors when trying to run the data sets through the models
df1 = df1.dropna()

# X and y assigned with the data required, X being the independant variables and y being the
# dependant variable
# i.e. our output (y) is dependant on the changing of the X values 
X = df1[['CL001','CL002','pH001','TP001','TCTEFF','FL001','TU001','CL_T1_VOL','FL004','LI001','CLDOSE','M001']]
y = df1[['CLTAR']]

# Dataset is broken up for training, testing and verification
# train_test_split is a function in Sklearn model selection for splitting data arrays into two subsets.
# for training data and for testing data. With this function, you don't need to divide the dataset manually.
# here our data is split 60/40, 60% trainging, 40% testing.
X_train, X_test, y_train,y_test = train_test_split(X, y, test_size = 0.4, random_state = 0)

# Assigning our model 'regressor' as a LinearRegression() model
regressor = LinearRegression()

# Fitting your model, using the .fit() method on the training data is the training part of the modeling process.
# It finds the coefficients for the equation specified via the algorithm being used in our case linear regression
regressor.fit(X_train, y_train)

# Testing the training and testing set predictions using the .predict() method
# enables us to predict the labels of the data values on the basis of the trained model.
Y_pred = regressor.predict(X_train)
#print(Y_pred)
#print('-------------------------------')
y_pred = regressor.predict(X_test)
#print(y_pred)
#print('-------------------------------')

# Main operational logic
# Loops forever
while True:

    # Data tags are filled by calling the PLC_tasks() along with the desired PLC IP address,target memory word, data length
    # being passed to the functions
    SP23 = PLC_Tasks(IP,5524,2)
    CL001_IP = PLC_Tasks(IP,4110,2)
    CL002_IP = PLC_Tasks(IP,4130,2)
    pH001_IP = PLC_Tasks(IP,4310,2)
    TP001_IP = PLC_Tasks(IP,4290,2)
    TCTEFF_IP = PLC_Tasks(IP,2284,2)
    FL001_IP = PLC_Tasks(IP,4010,2)
    TU001_IP = PLC_Tasks(IP,4190,2)
    CL_T1_VOL_IP = PLC_Tasks(IP,5090,2)
    FL004_IP = PLC_Tasks(IP,4270,2)
    LI001_IP = PLC_Tasks(IP,4030,2)
    CLDOSE_IP = PLC_Tasks(IP,2216,2)
    M001_IP = PLC_Tasks(IP,2212,2)

	# Uncomment to use Data_Generator
	#CL001_IP,CL002_IP,pH001_IP,TP001_IP,TCTEFF_IP,FL001_IP,TU001_IP,CL_T1_VOL_IP,FL004_IP,LI001_IP,CLDOSE_IP,M001_IP = data_generator()
        
   	# Predicting on the data tags provided from either the Data_Generator function or the real read data
    predict = regressor.predict([[CL001_IP,CL002_IP,pH001_IP,TP001_IP,TCTEFF_IP,FL001_IP,TU001_IP,CL_T1_VOL_IP,FL004_IP,LI001_IP,CLDOSE_IP,M001_IP]])
        
    # Cleaning up to assign the Control setpoint suggestion 
    ClTar_Pred = predict.item(0)
    #print(ClTar_Pred)
    # Push the data to the Database_Update function to send the data to the cloud database
    Database_Update(tcteff=TCTEFF_IP,ph001=pH001_IP,tp001=TP001_IP,cl001=CL001_IP,cl002=CL002_IP,Cltar_Pred=ClTar_Pred,tu001=TU001_IP,fl001=FL001_IP,fl004=FL004_IP,li001=LI001_IP)








