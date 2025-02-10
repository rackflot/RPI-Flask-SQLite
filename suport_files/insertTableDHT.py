#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  insertTableDHT.py
#  
# Developed by Marcelo Rovai, MJRoBot.org @ 9Jan18
#  
# Insert dada on table "DHT_data" 

import time
import board
import mariadb
import sys

sys.path.append('/home/pi/Adafruit_DHT')
from DHT_DB import *
from MF_Functions import *

dbh = iDHT_DB()

dbh.add_data (GetTimeStamp(), 20.5, 30, 1, 1)

dbh.Commit()
dbh.close()
