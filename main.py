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
		access_token_secret=access['secret'],
		tweet_mode='extended')
	return api

api = load_api()

def replaceUrl(status):
	for url_obj in status.urls:
		status.full_text = status.full_text.replace(url_obj.url, url_obj.expanded_url)
	return status.full_text

def replaceMedia(status):
	for media_obj in status.media:
		if (media_obj.type == 'photo'):
			status.full_text = status.full_text.replace(media_obj.url, media_obj.expanded_url)
		elif (media_obj.type == 'video'):
			bitrate = 0
			video_url = ''
			for video_variant in media_obj.video_info['variants']:
				try:
					if (video_variant['bitrate'] > bitrate):
						video_url = video_variant['url']
				except KeyError as e:
					continue
			status.full_text = status.full_text.replace(media_obj.url, video_url)
	return status.full_text

def getThreadContent(last_id):
	statuses = []
	status = api.GetStatus(last_id)
	statuses.append(status.full_text)
	i = 0
	while (status.in_reply_to_status_id != None):
		print(status)
		if i > 10: break
		status = api.GetStatus(status.in_reply_to_status_id)
		statuses.append(status)
		i = i + 1


# status = replaceMedia(status)
# print(status.full_text)