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
from DHT_DB import *
from MF_Functions import * 

dbh = iDHT_DB()

from flask import Flask, render_template, request
app = Flask(__name__)
# app = Flask(appDhtWebServer)

# Retrieve data from database
def getData():
	"""
	# conn=sqlite3.connect('../sensorsData.db')
	# dbh.curs=dbh.cursor()

	for row in dbh.curs.execute("SELECT * FROM Actions ORDER BY time DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
		hum = row[2]
	dbh.close()
	"""
	#statement = "SELECT itime, itemp, ihumid FROM actions" # ORDER BY itime DESC LIMIT 1"	
	#statement = "SELECT itime, itemp, ihumid FROM actions ORDER BY itime DESC LIMIT 1"
	statement = "SELECT * FROM actions order by itime DESC LIMIT 1"
	#data = (itime, itemp, ihumid)
	dbh.cursor.execute(statement) #, data)
	dbh.conn.commit()
	for row in dbh.cursor: #.fetchall():
		print(row[0], row[1], row[2]) #, row[3], row[4]) #setp=' ')

	return row[0], row[1], row[2]

# main route 
@app.route("/")
def index():
	ilast = GetTimeStamp()
	itime, itemp, ihumid = getData()
	templateData = {
	  'time'	: itime,
      'temp'	: itemp,	
      'humid'	: ihumid,
      'last'	: ilast
	}
	#print(templateData)
	return render_template('index.html', **templateData)


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=False)

