#!/usr/bin/env python

import requests
import argparse
import sys
from xml.dom import minidom

# Exit statuses recognized by Nagios
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2

#Parsing arguments
parser = argparse.ArgumentParser(description='Get NGAS Status and SubStatus')
parser.add_argument('-w', '--warning', action='store_true',help='Throw warning when Sub Status is busy')
#Changing arguments to required arguments (not optionals)
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('-H', '--hostname', type=str,required=True, help='NGAS Address')
requiredNamed.add_argument('-p', '--port', type=int, required=True, help='NGAS Port')
args = parser.parse_args()
try:	
	server = str(args.hostname).replace('http://','')
	port = str(args.port)

	#Making HTTP GET request
	r = requests.get('http://'+server+':'+port+'/STATUS')
	res = r.content
	#Parsing Response
	data = minidom.parseString(res)
	data = data.getElementsByTagName('Status')[0]
	data = data.attributes
	state = data['State'].value
	subState = data['SubState'].value
	
	#Sending information
	if state == 'ONLINE' and subState == 'IDLE':
		print("Ngas Online and IDLE |status=1 subStatus=1")
		sys.exit(OK)
	elif state == 'ONLINE' and subState != 'IDLE':
		if args.warning is None:
			print("Ngas Online and BUSY |status=1 sub_status=0")		
			sys.exit(OK)
		else:
			print("Ngas Online and BUSY |status=1 sub_status=0")
			sys.exit(WARNING)     

	else:
		print("Ngas Offline |status=0 sub_status=-1")
		sys.exit(CRITICAL)
except Exception as e:
	#If something go wrong in the HTTP GET Request
	print("Can't connect to server: "+str(e)+"|status=0 sub_status=-1")
	sys.exit(UNKNOWN)
