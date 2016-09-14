# filter = !17vhT8QOUm)koH5(u-VKOO052pl0CqLsE)qJhVj8Pg-YDP
import os, time
import requests
import json
import pprint

os.environ['TZ']='UTC'

# Filtering options
pagesize = 100
filter = '!17vhT8QOUm)koH5(u-VKOO052pl0CqLsE)qJhVj8Pg-YDP'
order = 'desc'
sort = 'votes'
site = 'stackoverflow'

# Converts date into epoch 
cur_year = 2016
from_date = '%s-01-01'
to_date = '%s-12-31'
date_format = '%Y-%m-%d'

# Initial URL
url = 'https://api.stackexchange.com/2.2/questions'
payload = {'pagesize': pagesize, 'order': order, 'sort': sort, 'site': site,
'filter': filter}

def update_year(year):
	"""Change the from and to date using UTC epoch"""
	payload['fromdate'] = int(time.mktime(time.strptime(from_date % year, date_format)))
	payload['todate'] = int(time.mktime(time.strptime(to_date % year, date_format)))

def generate_json(year):
	"""Attempts to generate JSON file from 2007-2016."""
	while(year >= 2007):
		update_year(year)

		# Sends a GET request to stackexchange API.
		# Example: https://api.stackexchange.com/2.2/questions?pagesize=100&fromdate=1356998400&todate=1388448000&order=desc&sort=votes&site=stackoverflow&filter=!17vhT8QOUm)koH5(u-VKOO052pl0CqLsE)qJhVj8Pg-YDP
		res = requests.get(url, params=payload)

		# Write json result into a json file
		file_name = 'data_' + str(year) + '.json'
		with open(file_name, 'w') as output:
			json.dump(res.json(), output)
		year -= 1

def check_questions(year):
	while(year >= 2007):
		file_name = 'data_' + str(year) + '.json'
		with open(file_name) as input:
			data = json.load(input)
		print 'Number of questions for year %d: %d ' % (year, 
			len(data['items']))
		year -= 1
		

#generate_json(2016)
check_questions(2016)

