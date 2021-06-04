# Programmer: Jonathan Logue
# Date: 17/3/2021
# Project: Sligo IT Final Year project - CHLORINE DISINFECTION SYSTEM DATA ANALYSIS & CONTROL
#
# Code Description: This code is running on the On-Site RPI4 & its task is to produce a toggling
# heartbeat every few seconds & write this heartbeat to the cloud database to provide an indication of 
# health. The heartbeat is dependant on an internet connection so we run a request.get() method to 
# basically ping google with a GET request to get data from a specified resource, in our case 
# google.com




# Importing librarys
import time 
import requests
from firebase import firebase

# Assigning the firebase address reference
firebase = firebase.FirebaseApplication('https://data-793f6-default-rtdb.firebaseio.com/',None)

# Assigning google.com as the url & our timeout value for the GET request
url = "http://www.google.com"
timeout = 5

# Loop forever
while True:
	# Try the GET request, if successful set WIFI_STATUS to TRUE
	try:
		request = requests.get(url, timeout=timeout)
		print("Connected to the Internet")
		WIFI_STATUS = True
	# If it fails then WIFI_STATUS = FALSE	
	except (requests.ConnectionError, requests.Timeout) as exception:
		print("No internet connection.")
		WIFI_STATUS = False

	#Toogling bit if WIFI = True	
	if(WIFI_STATUS==True):

		# Set bit to 0 
		bit = False
		#if bit is false the heartbeat = 0 & put this data to the database
		if(bit==False):
			heartbeat = 0
			print(bit,heartbeat)
		result = firebase.put('/SITE_Pi_STATUS/','Heartbeat_RTU',heartbeat) #update data

		# Pause program
		time.sleep(2)

		# Toggle the bits state
		bit = not bit
		# if the bit is toggled, heartbeat set to 1 & put this data to the database
		if(bit==True):
			heartbeat = 1
			print(bit,heartbeat)
		result = firebase.put('/SITE_Pi_STATUS/','Heartbeat_RTU',heartbeat) #update data
		time.sleep(2)
	else:
		print("Loop exited")
		time.sleep(5)
		


	


	



	


