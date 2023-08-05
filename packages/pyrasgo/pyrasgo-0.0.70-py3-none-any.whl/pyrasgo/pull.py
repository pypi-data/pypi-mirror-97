"""
Internal module to help consolidate all code related 
to pulling encrypted feature engineering scripts.
"""

import yaml
import requests
import warnings
import dill
import jsonpickle

warnings.filterwarnings('ignore') # Keep getting InsecureRequestWarning because hosting API on local without certs

def pull_code(feature_ids: list) -> list:
	# Load configuration file containing API keys and endpoints
	parse_config()
	parse_endpoints()
	# Verify that the API key provided is valid
	verify_key()
	# Key verified
	# Need to verify key with every request
	feature_funcs = [get_feature(x) for x in feature_ids]
	return feature_funcs

def get_feature(feature_id: str) -> dict:
	feature_endpt = endpoints['rasgo_endpoints']['feature_pull']
	# The GET request should return a JSON that includes the feature UID, feature name, description, and jsonpickle object
	# The way we will enable users to actually use the feature scripts is as follows:
	# import jsonpickle
	# func = jsonpickle.decode(r.json()['func_header'])
	# func now has effectively replaced the function name and can be used with all its arguments i.e. func(a, b)
	r = requests.get(url=feature_endpt, params={'key': api_key, 'feature_id': feature_id}, verify=False)
	assert (r.status_code == 200), "Problem pulling feature. Please verify that the unique feature ID is correct."
	return dill.loads(jsonpickle.decode(r.content))

def verify_key():
	verify_endpt = endpoints['rasgo_endpoints']['verify']
	global api_key
	api_key = config['rasgo_credentials']['access_key']
	r = requests.get(url=verify_endpt, params={'key': api_key}, verify=False)
	assert (r.json()['success'] == True), "Problem validating API key. Please double check your API key." # Not a successful verification of API key
	print("\nSuccessfully validated API key.")

def parse_config():
	global config
	with open('..\\config\\config.yaml') as f:
		config = yaml.load(f)

def parse_endpoints():
	global endpoints
	with open('endpoints.yaml') as f:
		endpoints = yaml.load(f)


# EVERYTHING BELOW HERE IS FOR TESTING PURPOSES

def test_func_pull(feature_id):
	r = requests.get(url=endpoints['rasgo_endpoints']['feature_pull'], params={'key': api_key, 'feature_id': feature_id}, verify=False)
	func = dill.loads(jsonpickle.decode(r.content))
	return func

def dark_sky_sample():
	import pandas as pd
	secret = '4e79a3dd798e30beb50c84a3b37bd5a0'
	latitude = '43.142'
	longitude = '-85.049'
	time = '1550008800'
	url = f'https://api.darksky.net/forecast/{secret}/{latitude},{longitude},{time}'
	r = requests.get(url)
	df = pd.DataFrame(r.json()['hourly']['data'])
	return df

def run_test(feature_id):
	# Load configuration file containing API keys and endpoints
	parse_config()
	parse_endpoints()
	# Verify that the API key provided is valid
	verify_key()
	# Get base Dark Sky data
	# base_df = dark_sky_sample()
	# print('\n\nRaw DF from Dark Sky API')
	# print(base_df.head())
	# Retreive function
	func = test_func_pull(feature_id)
	return func
	# new_df = func(base_df)
	# print('\n\nFeature engineered DF after Dark Sky')
	# print(new_df.head())


# run_test()