import urllib
import json
from pprint import pprint
import csv
import os
import sys


def main():
	if os.environ.get('LIBRATO_USER') == None or os.environ.get('LIBRATO_TOKEN') == None or os.environ.get('LIBRATO_METRICS') == None:
		print "Missing env vars ( LIBRATO_USER, LIBRATO_TOKEN or LIBRATO_METRICS )"
		sys.exit(0)
	librato_email = os.environ['LIBRATO_USER']
	librato_token = os.environ['LIBRATO_TOKEN']
	librato_metrics = os.environ['LIBRATO_METRICS'].split(",")

	dictionary = {}
	fp = open('api_calls.csv','wb')
	a = csv.writer(fp, delimiter = ",")
	for name in librato_metrics:
		link = 'https://' + librato_email + ':' + librato_token + '@metrics.librato.com/metrics-api/v1/metrics/' + name + '?resolution=60&start_time=1424268251'
		data = parsingData(link)
		for item in data['measurements']['loveos']:
			if item['measure_time'] not in dictionary.keys():
				dictionary[item['measure_time']] = {}
			dictionary[item['measure_time']][name] = item['value']
	for item in dictionary.keys():
		row = []
		row.append(item)
		for name in librato_metrics:
			row.append(dictionary[item][name])
		a.writerow(row)

def parsingData(link):
	f = urllib.urlopen(link)
	readLink = f.read()
	calls = json.loads(readLink)
	return calls

if __name__=='__main__':
	main()