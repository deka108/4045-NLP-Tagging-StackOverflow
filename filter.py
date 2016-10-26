import json
import os
import pprint
import requests
import time

os.environ['TZ'] = 'UTC'
data_dir = 'data'
file_name_year = 'data_%s'
file_name_year_java = 'data_%s_java'
file_name_month = 'data_%s-%s'
file_name_month_java = 'data_%s-%s_java'
json_suffix = '.json'

# Filtering options
pagesize = 100
page = 1
filter = '!)EhwLl5mQ7SRRT.giqkyY*Ml6ZLhMFIWSL4731oh8m9wwZ.ra'  # with count
order = 'desc'
sort = 'votes'
site = 'stackoverflow'
tagged = 'java'

# Initial URL + payload
url = 'https://api.stackexchange.com/2.2/questions'
payload = {'pagesize': pagesize, 'order': order, 'sort': sort, 'site': site,
           'filter': filter}

# Date formats
from_date = 'from_date'
to_date = 'to_date'

first_half = {from_date: '%s-01-01', to_date: '%s-06-30'}
sec_half = {from_date: '%s-07-01', to_date: '%s-12-31'}
date_year = {from_date: '%s-01-01', to_date: '%s-12-31'}

date_format = '%Y-%m-%d'
base_year = 2008
base_halfyear = 2011


def get_format_per_month(year):
    per_month = [
        {from_date: '%s-01-01', to_date: '%s-01-31'},
        {from_date: '%s-02-01', to_date: '%s-02-28'},
        {from_date: '%s-03-01', to_date: '%s-03-31'},
        {from_date: '%s-04-01', to_date: '%s-04-30'},
        {from_date: '%s-05-01', to_date: '%s-05-31'},
        {from_date: '%s-06-01', to_date: '%s-06-30'},
        {from_date: '%s-07-01', to_date: '%s-07-31'},
        {from_date: '%s-08-01', to_date: '%s-08-31'},
        {from_date: '%s-09-01', to_date: '%s-09-30'},
        {from_date: '%s-10-01', to_date: '%s-10-31'},
        {from_date: '%s-11-01', to_date: '%s-11-30'},
        {from_date: '%s-12-01', to_date: '%s-12-31'}
    ]

    if year % 4 == 0:
        per_month[1] = {from_date: '%s-02-01', to_date: '%s-02-29'}

    return per_month


def update_year(format, year):
    """Updates the from and to date as UTC epoch per year."""
    payload['fromdate'] = int(
        time.mktime(time.strptime(format[from_date] % year, date_format)))
    payload['todate'] = int(
        time.mktime(time.strptime(format[to_date] % year, date_format)))


def update_half_year(year, is_first_half):
    """Updates the from and to date as UTC epoch per half year."""
    if (is_first_half):
        half = first_half
    else:
        half = sec_half

    update_year(half, year)


def generate_json_per_halfyear(year, file_format=file_name_month):
    """Generates JSON file per 6 months from 01/01/11 - 31/12/15."""
    is_first_half = False
    half = first_half

    while (year >= base_halfyear):
        update_half_year(year, is_first_half)

        # Sends a GET request via StackExchange API.
        # Example: https://api.stackexchange.com/2.2/questions?pagesize=100&fromdate=1356998400&todate=1388448000&order=desc&sort=votes&site=stackoverflow&filter=!17vhT8QOUm)koH5(u-VKOO052pl0CqLsE)qJhVj8Pg-YDP
        res = requests.get(url, params=payload)

        # Write JSON result into a JSON file
        if is_first_half:
            frmdate = first_half[from_date] % year
            todate = first_half[to_date] % year
            year -= 1
        else:
            frmdate = sec_half[from_date] % year
            todate = sec_half[to_date] % year

        file_name = file_format % (frmdate, todate) + json_suffix

        path = os.path.join(data_dir, file_name)
        with open(path, 'w') as output:
            json.dump(res.json(), output)

        is_first_half = not is_first_half


def generate_json_per_halfyear_tag(year):
    payload['tagged'] = 'java'
    generate_json_per_halfyear(year, file_name_month_java)
    del payload['tagged']


generate_json_per_halfyear_java_tag(2015)