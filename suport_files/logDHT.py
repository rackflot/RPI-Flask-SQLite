#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  logDHT.py
#
#  Developed by Marcelo Rovai, MJRoBot.org @ 10Jan18
#  
#  Capture data from a DHT22 sensor and save it on a database

import time
import sqlite3
import adafruit_dht
import board

dbname='sensorsData.db'
sampleFreq = 1 # time in seconds

def initDHT():
	global DHT22Sensor
	DHT22Sensor = adafruit_dht.DHT22(board.D4)
	print("initialized DH22")

# get data from DHT sensor
def getDHTdata():		
	# DHT22Sensor = adafruit_dht.DHT22
	# DHTpin = 16
	#hum, temp = adafruit_dht.read_retry(DHT22Sensor, DHTpin)
	try:
		temp = DHT22Sensor.temperature
		hum  = DHT22Sensor.humidity 
	except RuntimeError as error:
		# Errors happen fairly often, DHT's are hard to read, just keep going
		cError = error.args[0]
		print(cError)
		time.sleep(2.0)    
		#continue
	except Exception as error:
		DHT22Sensor.exit()
		raise error
	except:
		print(error.args[0])
	else:
		if hum is not None and temp is not None:
			hum = round(hum)
			temp = round(temp, 1)
	return temp, hum

# log sensor data on database
def logData (temp, hum):
	
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	
	curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum))
	conn.commit()
	conn.close()

# display database data
def displayData():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	print ("\nEntire database contents:\n")
	for row in curs.execute("SELECT * FROM DHT_data"):
		print (row)
	conn.close()

# main function
def main():
	initDHT()
	while True:
		temp, hum = getDHTdata()
		logData (temp, hum)
		displayData()
		time.sleep(sampleFreq)

# ------------ Execute program 
main()

