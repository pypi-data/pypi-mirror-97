import flask
from flask import request, jsonify
import dill
import jsonpickle

app = flask.Flask(__name__)

@app.route('/verify')
def verify():
	return jsonify(success=request.args['key'] == 'bce2dad0-39dc-4840-9e47-3929cbf20cc0')

def verify_key(key):
	return key == 'bce2dad0-39dc-4840-9e47-3929cbf20cc0'

@app.route('/pull')
def pull():
	assert verify_key(request.args['key']), 'Bad API key.'
	assert 'feature_id' in request.args.to_dict(), 'No feature ID parameter included in request.' 
	return func_handler(request.args['feature_id'])

def func_handler(feature_id):
	if feature_id == 't1gnamzko8bco7795p1s':
		return jsonpickle.encode(dill.dumps(t1gnamzko8bco7795p1s))
	else:
		return 'DID NOT WORK'

def t1gnamzko8bco7795p1s(df):
	import pandas as pd
	hourly_temp_df = df[['time', 'icon']]
	hourly_temp_df['time'] = pd.to_datetime(hourly_temp_df['time'], unit='s').dt.strftime("%Y-%m-%d %H:%M")
	return hourly_temp_df

def id(name):
	if name == 'Jared':
		return 'CEO'
	elif name == 'Patrick':
		return 'CTO'
	elif name == 'Will':
		return 'SAIA Driver'

app.run(host='0.0.0.0', port=6500, ssl_context='adhoc', debug=True)
