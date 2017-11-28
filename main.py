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
		status.full_text = status.full_text.replace(url_obj.url, '<a href="' + url_obj.expanded_url + '">' + url_obj.expanded_url + '</a>')
	return status.full_text

def replaceMedia(status):
	for media_obj in status.media:
		if (media_obj.type == 'photo'):
			status.full_text = status.full_text.replace(media_obj.url, '<p><img src="' + media_obj.media_url_https + '"></p>')
		elif (media_obj.type == 'video'):
			bitrate = 0
			video_url = ''
			for video_variant in media_obj.video_info['variants']:
				try:
					if (video_variant['bitrate'] > bitrate):
						video_url = video_variant['url']
				except KeyError as e:
					continue
			status.full_text = status.full_text.replace(media_obj.url, '<p><video controls=""><source src="' + video_url + '"></video></p>')
	return status.full_text

def formatStatus(status):
	status_str = ''
	if (len(status.urls) != 0):
		status_str = status_str + replaceUrl(status)
	if (status.media != None):
		status_str = status_str + replaceMedia(status)
	if (status.media == None and len(status.urls) == 0):
		status_str = status_str + status.full_text
	return '</p>' + status_str + '</p>'


def getThreadContent(last_id):
	statuses = []
	status = api.GetStatus(last_id)
	statuses.append(formatStatus(status))
	i = 0
	while (status.in_reply_to_status_id != None):
		if i > 10: break
		status = api.GetStatus(status.in_reply_to_status_id)
		statuses.append(formatStatus(status))
		i = i + 1
	html_str = ''
	for status_str in reversed(statuses):
		html_str = html_str + status_str
	return html_str
