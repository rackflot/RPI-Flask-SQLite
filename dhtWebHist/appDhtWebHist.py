#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  appDHT_v1.py
#  
#  Created by MJRoBot.org 
#  10Jan18

'''
	RPi WEb Server for DHT captured data with Graph plot  
'''

# Add in directory
import sys
sys.path.append('/home/pi/Adafruit_DHT')

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from flask import Flask, render_template, send_file, make_response, request
from DHT_DB import *
from MF_Functions import * 

dbh = iDHT_DB()

app = Flask(__name__)
'''
import sqlite3
conn=sqlite3.connect('../sensorsData.db')
curs=conn.cursor()
'''
# Retrieve LAST data from database
def getLastData():
	statement = "SELECT * FROM actions ORDER BY itime DESC LIMIT 1"
	dbh.cursor.execute(statement)
	dbh.conn.commit()
	for row in dbh.cursor: #  ("SELECT * FROM actions ORDER BY itime DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
		hum = row[2]
	#conn.close()
	return time, temp, hum


def getHistData (numSamples):
	statement = "SELECT * FROM actions ORDER BY itime DESC LIMIT "+str(numSamples)
	dbh.cursor.execute(statement)
	dbh.conn.commit()
	# curs.execute("SELECT * FROM actions ORDER BY timestamp DESC LIMIT "+str(numSamples))
	# data = dbh.curs.fetchall()
	dates = []
	temps = []
	hums = []
	for row in dbh.cursor:
		dates.append(row[0])
		temps.append(row[1])
		hums.append(row[2])
	return dates, temps, hums

def maxRowsTable():
	statement = "select COUNT(itemp) from  actions"
	dbh.cursor.execute(statement)
	dbh.conn.commit() 
	for row in dbh.cursor: #.execute("select COUNT(itemp) from actions"):
		maxNumberRows=row[0]
	return maxNumberRows

#initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
	numSamples = 100
	
	
# main route 
@app.route("/")
def index():
	
	time, temp, humid = getLastData()
	templateData = {
	  'time'		: time,
      'temp'		: temp,
      'hum'			: humid,
      'numSamples'	: numSamples
	}
	return render_template('index.html', **templateData)


@app.route('/', methods=['POST'])
def my_form_post():
	global numSamples 
	numSamples = int (request.form['numSamples'])
	numMaxSamples = maxRowsTable()
	if (numSamples > numMaxSamples):
		numSamples = (numMaxSamples-1)

	time, temp, hum = getLastData()
	templateData = {
	  'time'		: time,
      'temp'		: temp,
      'hum'			: hum,
      'numSamples'	: numSamples
	}
	return render_template('index.html', **templateData)
	
	
@app.route('/plot/temp')
def plot_temp():
	times, temps, hums = getHistData(numSamples)
	ys = temps
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature [°C]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/hum')
def plot_hum():
	times, temps, hums = getHistData(numSamples)
	ys = hums
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Humidity [%]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=False)

