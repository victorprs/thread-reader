import twitter
import json

def load_api():
	with open('secret.json') as f:
		secret = json.load(f)
	with open('token.json') as f2:
		access = json.load(f2)

	api = twitter.Api(consumer_key=secret['key'],
		consumer_secret=secret['secret'],
		access_token_key=access['key'],
		access_token_secret=access['secret'])
	return api

api = load_api()