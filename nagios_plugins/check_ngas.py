#!/usr/bin/env python

import requests
import sys
from xml.dom import minidom
# Exit statuses recognized by Nagios
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2

try:
	params = sys.argv
	server = str(params[1])
	port = str(params[2])
	r = requests.get('http://'+server+':'+port+'/STATUS')
	res = r.content
	data = minidom.parseString(res)
	data = data.getElementsByTagName('Status')[0]
	data = data.attributes
	state = data['State'].value
	subState = data['SubState'].value
	
	if state == 'ONLINE' and subState == 'IDLE':
		print("Ngas Online and IDLE |status=1 subStatus=1")
		sys.exit(0)
	elif state == 'ONLINE' and subState != 'IDLE':
		print("Ngas Online and BUSY |status=1 sub_status=0")		
		sys.exit(0)
	else:
		print("Ngas Offline |status=0 sub_status=-1")
		sys.exit(2)
except Exception as e:
	print("Can't connect to server: "+str(e)+"|status=0 sub_status=-1")
	sys.exit(2)
