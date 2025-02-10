#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lastLogDataTableDHT.py
#  
# Query dada from last input on table "DHT_data" 

import time
import board
import mariadb
import sys

sys.path.append('/home/pi/Adafruit_DHT')
from DHT_DB import *
from MF_Functions import *

dbh = iDHT_DB()

# dbh.get_data()
dbh.cursor.execute("SELECT * FROM actions ORDER BY time DESC LIMIT 1")
dbh.conn.commit()
data = dbh.cursor.fetchall()
for row in data: #dbh.cursor.execute("SELECT * FROM actions"): # ORDER BY timestamp DESC LIMIT 1"):
    print (row)
