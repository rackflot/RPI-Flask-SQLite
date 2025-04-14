#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  insertDataTableDHT.py
#  
#  Developed by Marcelo Rovai, MJRoBot.org @ 9Jan18
#  
#  Query dada on table "DHT_data" 
import time
import board
import mariadb
import sys

# use the original files, add this dir.
sys.path.append('/home/pi/Adafruit_DHT')
from DHT_DB import *
from MF_Functions import *

dbh = iDHT_DB()
# dbh.add_data(GetTimeStamp(), temperature_f, humidity, 4, 5)


#def add_data (temp, hum):
#   curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum))
#    conn.commit()

dbh.add_data (GetTimeStamp(), 20.5, 30, 1, 1)
dbh.add_data (GetTimeStamp(), 25.8, 40, 1, 1)
dbh.add_data (GetTimeStamp(), 30.3, 50, 1, 1)


print ("\nEntire database contents:\n")
dbh.get_data()

# for row in curs.execute("SELECT * FROM DHT_data"):
#    print (row)


# conn.close()
