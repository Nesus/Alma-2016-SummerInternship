#!/usr/bin/env python

import requests
import sys
from xml.dom import minidom

requests.packages.urllib3.disable_warnings()
# Exit statuses recognized by Nagios
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2
username = 'monarcs'
password = 'a1maarcs'

try:
	params = sys.argv
	sensor = int(params[1])
	warn = int(params[2])
	crit = int(params[3])
	sensor_request = 'https://prtg.alma.cl/api/getsensordetails.json'

	s_params = {
		'id':sensor,
		'username': username,
		'password': password
	}
	s = requests.get(sensor_request,params= s_params, verify= False)
	s = s.json()['sensordata']
	up = 1 if s['statustext'] == 'Up' else 0
	ping = float(s['lastvalue'].split()[0])
	if up and ping < warn:
		print("Up ping:"+str(ping)+" | status=1 latency="+str(ping))
		sys.exit(OK)
	elif up and ping > warn and ping < crit:
		print("Up ping:"+str(ping)+" | status=1 latency="+str(ping))
		sys.exit(WARNING)
	elif up and ping > crit:
		print("Up ping:"+str(ping)+" | status=1 latency="+str(ping))
		sys.exit(CRITICAL)
	else:
		print("Down | status=0")
		sys.exit(CRITICAL)

except Exception as e:
	print("Error : "+str(e)+"| status=0")
	sys.exit(2)
