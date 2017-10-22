#!/usr/bin/python
"""
Queries some API endpoints for the most important data and saves it to a sqlite database
for easy access. Should be run regularly, e.g. every 5 minutes.
"""

import time
import collections
import requests
import sys

hostname = "fronius"
pvStat = sys.argv[1]

data = collections.OrderedDict()
current_time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def get_data(url):
	try:
		r = requests.get(url, timeout=10)
		r.raise_for_status()
		return r.json()	
	except requests.exceptions.Timeout:
		print("Timeout requesting {} at {}".format(url, current_time_string))
	except requests.exceptions.RequestException as e:
		print("requests exception {} at {}".format(e, current_time_string))

	# if we get no data, we exit directly
	return exit()


# Powerflow
starttime = time.time()

data['timestamp'] = time.time()

powerflow_url = "http://" + hostname + "/solar_api/v1/GetPowerFlowRealtimeData.fcgi"
powerflow_data = get_data(powerflow_url)

data['powerflow_timestamp'] = powerflow_data['Head']['Timestamp']
data['powerflow_mode'] = powerflow_data['Body']['Data']['Site']['Mode']
data['powerflow_P_Grid'] = powerflow_data['Body']['Data']['Site']['P_Grid']
data['powerflow_P_Load'] = powerflow_data['Body']['Data']['Site']['P_Load']
data['powerflow_P_Akku'] = powerflow_data['Body']['Data']['Site']['P_Akku']
data['powerflow_P_PV'] = powerflow_data['Body']['Data']['Site']['P_PV']
data['powerflow_E_Day'] = powerflow_data['Body']['Data']['Site']['E_Day']
data['powerflow_E_Year'] = powerflow_data['Body']['Data']['Site']['E_Year']
data['powerflow_E_Total'] = powerflow_data['Body']['Data']['Site']['E_Total']

print data[pvStat]
