#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  appDhtWebServer.py
#  
#  Created by MJRoBot.org 
#  10Jan18

'''
	RPi Web Server for DHT captured data  
'''
# import time
# import board
# import mariadb
import sys

sys.path.append('/home/pi/Adafruit_DHT')
sys.path.append('/home/pi/RPI_Flask_SQLite/dhtWebServer/')
# from DHT_DB import *
from MF_Functions import * 

# dbh = iDHT_DB()

from flask import Flask, render_template, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('/home/pi/RPI_Flask_SQLite/sensorsData.db', check_same_thread = False)
curs=conn.cursor()


# Retrieve data from database
def getData():
	# conn=sqlite3.connect('../sensorsData.db')
	# dbh.curs=dbh.cursor()

	for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
		hum = row[2]
		print(str(row[0]) + " " + str(row[1]) + " " + str(row[2])) 
	return time, temp, hum


# main route 
@app.route("/")
def index():
	ilast = GetTimeStamp()
	time, temp, hum = getData()
	templateData = {
	  'time'	: time,
      'temp'	: temp,	
      'hum'		: hum,
      'last'	: ilast
	}
	#print(templateData)
	return render_template('index.html', **templateData)


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=False)

