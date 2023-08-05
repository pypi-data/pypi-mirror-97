from pyrasgo.get import get_feature
import requests

# EVERYTHING BELOW FOR TESTING
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


base_df = dark_sky_sample()
print('\n\nRaw DF from Dark Sky API')
print(base_df.head())
func = get_feature(['t1gnamzko8bco7795p1s'])[0] #This is the only Rasgo interaction the user will have
new_df = func(base_df)
print('\n\nFeature engineered DF after Dark Sky')
print(new_df.head())
