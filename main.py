import twitter
import json

with open('secret.json') as f:
	secret = json.load(f)

print (secret["key"])