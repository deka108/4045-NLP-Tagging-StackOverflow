import json
import os
import pprint
import requests
import time

os.environ['TZ']='UTC'
data_dir = 'data'

# Filtering options
pagesize = 100
# filter w/o answer count = !17vhT8QOUm)koH5(u-VKOO052pl0CqLsE)qJhVj8Pg-YDP
filter = '!)EhwLl5mQ7SRRT.giqkyY*Ml6ZLhMFIWPHEQ-OGv88TMTWrEL' # with count
order = 'desc'
sort = 'votes'
site = 'stackoverflow'

# Date formats
first_half = {'from_date': '%s-01-01', 'to_date': '%s-06-30'}
sec_half = {'from_date': '%s-07-01', 'to_date': '%s-12-31'}
from_date = '%s-01-01'
to_date = '%s-12-31'
date_format = '%Y-%m-%d'
base_year = 2008
base_halfyear = 2011

# Initial URL + payload
url = 'https://api.stackexchange.com/2.2/questions'
payload = {'pagesize': pagesize, 'order': order, 'sort': sort, 'site': site, 'filter': filter}

def update_year(year):
	"""Updates the from and to date as UTC epoch per year."""
	payload['fromdate'] = int(time.mktime(time.strptime(from_date % year, date_format)))
	payload['todate'] = int(time.mktime(time.strptime(to_date % year, date_format)))

def update_half_year(year, is_first_half):
	"""Updates the from and to date as UTC epoch per half year."""
	if (is_first_half):
		half = first_half
	else:
		half = sec_half

	payload['fromdate'] = int(time.mktime(time.strptime(half['from_date'] % year, date_format)))
	payload['todate'] = int(time.mktime(time.strptime(half['to_date'] % year, date_format)))

def generate_json_per_year(year):
	"""Attempts to generate JSON file per year from 01/01/08 - 31/12/16."""
	while(year >= base_year):
		update_year(year)

		# Sends a GET request via StackExchange API.
		# Example: https://api.stackexchange.com/2.2/questions?pagesize=100&fromdate=1356998400&todate=1388448000&order=desc&sort=votes&site=stackoverflow&filter=!17vhT8QOUm)koH5(u-VKOO052pl0CqLsE)qJhVj8Pg-YDP
		res = requests.get(url, params=payload)

		# Write JSON result into a JSON file
		file_name = 'data_' + str(year) + '.json'
		path = os.path.join("data", file_name)
		with open(path, 'w') as output:
			json.dump(res.json(), output)
		
		year -= 1

def generate_json_per_halfyear(year):
	"""Attempts to generate JSON file per 6 months from 01/01/11 - 31/12/15."""
	is_first_half = False

	while(year >= base_halfyear):
		update_half_year(year, is_first_half)

		# Sends a GET request via StackExchange API.
		# Example: https://api.stackexchange.com/2.2/questions?pagesize=100&fromdate=1356998400&todate=1388448000&order=desc&sort=votes&site=stackoverflow&filter=!17vhT8QOUm)koH5(u-VKOO052pl0CqLsE)qJhVj8Pg-YDP
		res = requests.get(url, params=payload)

		# Write JSON result into a JSON file
		if is_first_half:
			file_name = 'data_first_half_' + str(year) + '.json'
			year -= 1
		else:
			file_name = 'data_sec_half_' + str(year) + '.json'

		path = os.path.join("data", file_name)

		with open(path, 'w') as output:
			json.dump(res.json(), output)
		
		is_first_half = not is_first_half

def check_questions_per_year(year):
	"""Validates that number of question posts per year are 100."""
	while(year >= base_year):
		file_name = 'data_' + str(year) + '.json'
		path = os.path.join(data_dir, file_name)

		with open(path) as input:
			data = json.load(input)
		print 'Number of questions for year %d: %d ' % (year, 
			len(data['items']))

		year -= 1

def check_questions_per_halfyear(year):
	"""Validates that number of question posts per half year are 100."""
	is_first_half = False
	time_frame = ''

	while(year >= base_halfyear):
		cur_year = year
		
		if is_first_half:
			file_name = 'data_first_half_' + str(cur_year) + '.json'
			time_frame = 'first half'
			year -= 1
		else:
			file_name = 'data_sec_half_' + str(cur_year) + '.json'
			time_frame = 'sec half'

		path = os.path.join(data_dir, file_name)

		with open(path) as input:
			data = json.load(input)

		print 'Number of question posts in %s of %d: %d ' % (time_frame, cur_year, len(data['items']))

		is_first_half = not is_first_half
		

#generate_json_per_year(2016)
check_questions_per_year(2016)
#generate_json_per_halfyear(2015)
check_questions_per_halfyear(2015)
