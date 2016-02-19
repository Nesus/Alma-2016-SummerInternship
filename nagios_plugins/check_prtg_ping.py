#!/usr/bin/env python

import requests
import argparse
import sys
import os
from xml.dom import minidom

requests.packages.urllib3.disable_warnings()
# Exit statuses recognized by Nagios
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2

#Parsing arguments
parser = argparse.ArgumentParser(description='Get Latency and Status of a PRTG Ping Sensor')
parser.add_argument('-u', '--user', type=str, help='PRTG Username')
parser.add_argument('-p', '--password', type=str, help='PRTG Password')
parser.add_argument('-H', '--server', type=str, help='PRTG Address')

#Required arguments
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('sensor_id', type=int, help="PRTG Ping Sensor id")
requiredNamed.add_argument('-w', '--warning', type=int, required=True, help='Warning threshold for latency (ms)')
requiredNamed.add_argument('-c', '--critical', type=int, required=True, help='Critical threshold for latency (ms)')

args = parser.parse_args()

if args.user is None:
	username = os.environ['PRTG_USERNAME']
else:
	username = args.user
if args.password is None:
	password = os.environ['PRTG_PASSWORD']
else:
	password = args.password

try:
	sensor = args.sensor_id
	warn = args.warning
	crit = args.critical
	if args.server is None:
		sensor_request = 'https://prtg.alma.cl/api/getsensordetails.json'
	else:
		if ('http://' not in args.server) or ('https://' not in args.server):
			sys.exit(UNKNOWN)
		sensor_request = args.server + '/api/getsensordetails.json'

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
		print("Up ping:"+str(ping)+" ms | status=1 latency="+str(ping))
		sys.exit(OK)
	elif up and ping > warn and ping < crit:
		print("Up ping:"+str(ping)+" ms | status=1 latency="+str(ping))
		sys.exit(WARNING)
	elif up and ping > crit:
		print("Up ping:"+str(ping)+" ms | status=1 latency="+str(ping))
		sys.exit(CRITICAL)
	else:
		print("Down | status=0")
		sys.exit(CRITICAL)

except Exception as e:
	print("Error : "+str(e)+"| status=0")
	sys.exit(UNKNOWN)
