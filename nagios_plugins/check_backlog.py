#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2013 Unknown <abarrien@apo05.osf.alma.cl>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import cx_Oracle
import os
import argparse
import sys
import dateutil.parser

from datetime import datetime,timedelta

# Exit statuses recognized by Nagios
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2

#Default Days and Hours
DAYS = 1
HOURS = 0
OLDER_DAYS = 1
#Parsing arguments
parser = argparse.ArgumentParser(description='Get Backlog Size in a certain period of time')
parser.add_argument('arc', type=str, help='ARC Shortname')
parser.add_argument('-d','--days', type=int, help='Days to consult backlog size (Default 15 days)')
parser.add_argument('-hs','--hours', type=int, help='Days to consult backlog size (Default 0 days)')

parser.add_argument('-ol','--older', type=int, help='Sends Warning if a file is older than a numer of days before (default 1 day)')
parser.add_argument('-w','--warning', type=int, help='Add to warning alert if there is a big backlog (Size in GB)')
parser.add_argument('-c','--critical', type=int, help='Sends Critial Alert when there is a lot of files Stucked and the backlog size is Big (Integer: Amount of files)')


args = parser.parse_args()
#Checking if arc is on ARCS list
arc = args.arc.upper()
if arc not in ['EA','EU','NA']:
	print "ARC parameter is not correct"
	sys.exit(UNKNOWN)

#Checking that critical and warning is set
if (args.critical is not None) and (args.warning is None):
	print "Critical is set but warning not"
	sys.exit(UNKNOWN)

#Parsing Other arguments
if args.hours is not None:
	HOURS = args.hours
if args.days is not None:
	DAYS = args.days
if args.older is not None:
	OLDER_DAYS = args.older

#Connection info
dsn = '''(DESCRIPTION_LIST =
(FAILOVER = TRUE)
(LOAD_BALANCE = FALSE)
(DESCRIPTION =
  (ENABLE=BROKEN)
  (CONNECT_TIMEOUT=5)(RETRY_COUNT=3)  
  (ADDRESS = (PROTOCOL = TCP)(HOST = orasco.sco.alma.cl)(PORT = 1521))
  (CONNECT_DATA =
    (SERVER = DEDICATED)
    (SERVICE_NAME = ALMA.SCO.CL)
  )
)
(DESCRIPTION =
  (ENABLE=BROKEN)
  (CONNECT_TIMEOUT=5)(RETRY_COUNT=3)     
  (ADDRESS = (PROTOCOL = TCP)(HOST = orastbsco1.sco.alma.cl)(PORT = 1521))
  (CONNECT_DATA =
    (SERVER = DEDICATED)
    (SERVICE_NAME = ALMA.SCO.CL)
  )
)
)'''

#Creating Connection
orcl = cx_Oracle.connect('almasu', 'alma4dba', dsn)
cursor = orcl.cursor()
cursor.arraysize = 1000

#EA has ALMA2.ARC.EA
alma2 = '' if arc != 'EA' else '2'

#SQL Statement, modify if prefered, try to use the same order
#in the first select statement (SIZE, AMOUNT, MIN)
SQL = '''Select SUM(SIZE_IN_B), COUNT(*), MIN(ING_DATE) FROM
	(SELECT	SRC.FILE_SIZE SIZE_IN_B, SRC.INGESTION_DATE ING_DATE
	FROM NGAS.NGAS_FILES SRC
	WHERE INGESTION_DATE >:PERIOD
	AND FILE_ID || '.' || FILE_VERSION || '.' || CHECKSUM NOT IN
		(SELECT FILE_ID || '.' || FILE_VERSION || '.' || CHECKSUM
		FROM NGAS.NGAS_FILES@ALMA'''+alma2+'''.ARC.''' + arc + ''' 
		WHERE INGESTION_DATE >:PERIOD)
	ORDER BY SIZE_IN_B DESC)'''
PERIOD = (datetime.now() - timedelta(days=DAYS, hours= HOURS)).isoformat()
OLDER_PERIOD = (datetime.now() - timedelta(days=OLDER_DAYS)).isoformat()

try:
	#Sending SQL Query
	cursor.execute(SQL, PERIOD=PERIOD)
	backlog = cursor.fetchone()
	#Getting data and transforming Size in B to GB 
	size = backlog[0] if backlog[0] is not None else 0
	size = round(float(size)/1024/1024/1024,4)
	amount = backlog[1]
	min_date = backlog[2]
	
	msg = str(amount) + " files detected ("+str(size)+" GB)"
	perf_data = " |backlog_size="+str(size)+" files_detected="+str(amount)
	
	#Checking Warning and Critical
	if (min_date is not None) and (min_date < OLDER_PERIOD):
		d = min_date.split('.')[0]
		print_date = str(dateutil.parser.parse(d))
		older_msg = " some ingestion_date older than "+ str(OLDER_DAYS)+  " day" + ("s" if OLDER_DAYS > 1 else "") + " (" + print_date + ") "
		if args.warning is not None:
			if size > args.warning:
				print msg + older_msg + "over size threshold" + perf_data
				if args.critical is not None:
					if amount > args.critical:
						print msg + older_msg + "over size and amount threshold" + perf_data
						sys.exit(CRITICAL)
				sys.exit(WARNING)
		else:
			print msg + older_msg + perf_data
			sys.exit(WARNING)
	if amount == 0:
		print "No Files Detected" + perf_data
	else:
		print msg + perf_data
	sys.exit(OK)

	cursor.close()
	orcl.close()
	
except Exception,e:
	cursor.close()
	orcl.close()
	print "Problems connecting to ARC: "+arc+ " Error: "+ str(e)
	sys.exit(UNKNOWN)
