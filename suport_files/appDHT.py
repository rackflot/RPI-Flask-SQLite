#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  appDHT.py
#  

import time
import sqlite3
import adafruit_dht
import board

dbname='sensorsData2.db'
sampleFreq = 2 # time in seconds
DHT22Sensor = ""

def initDHT():
	global DHT22Sensor
	DHT22Sensor = adafruit_dht.DHT22(board.D4)
	print("initializedDH22")

# get data from DHT sensor
def getDHTdata():	
	# DHTpin = 4
	# hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
	temp = DHT22Sensor.temperature
	hum = DHT22Sensor.humidity 
	
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
		logData (temp, hum)

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
	for i in range (0,3):
		getDHTdata()
		time.sleep(sampleFreq)
	displayData()

# Execute program 
main()

