import twitter, json, csv
from urllib.parse import unquote

q = 'homepod'
count = 100
loop = 120

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

# Set the key and secret of your twitter developer  
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
						   CONSUMER_KEY, CONSUMER_SECRET)

# Get twitter API
twitter_api = twitter.Twitter(auth=auth)

# Create or open a csv file and write
# Set the csv delimiter with '|'
csvfile = open('tweets_7days.csv', 'a')
csvwriter = csv.writer(csvfile, delimiter='|')

# This function receive a string and replace its charater of '|', carriage return and line feed with black.
def getVal(val):
	clean = ""
	if val:
		val = val.replace('|', ' ')
		val = val.replace('\n', ' ')
		val = val.replace('\r', ' ')
		clean = val
	return clean

# This function receive a list of tweets, then write them into csv file.  
def tweetsWriter(tweets):
	for tweet in tweets:
		# if the field of coordinates is not none, then convert its value to a string
		if tweet['coordinates']:
			geocode = ",".jion(tweet['coordinates']['coordinates'])
		else:
			geocode = tweet['coordinates']

		# write the values to file
		csvwriter.writerow([
			tweet['id_str'],
			tweet['created_at'],
			geocode,
			getVal(tweet['user']['screen_name']),
			getVal(tweet['full_text']),
			getVal(tweet['user']['location']),
			tweet['user']['statuses_count'],
			tweet['user']['followers_count'],
			tweet['user']['friends_count'],
			tweet['user']['created_at']])

print ('Filtering the public timeline for track="%s"' % (q,))

# Search the tweets which inculde 'q', and the number is limited to 'count'.  
search_results = twitter_api.search.tweets(q=q, count=count, tweet_mode='extended') 
statuses = search_results['statuses']
tweetsWriter(statuses)
# Iterate through 'loop' more batches of results by following the cursor
number = 0
for _ in range(loop):
	number += len(statuses)
	print('Length of statuses', number) 
	try:
		next_results = search_results['search_metadata']['next_results'] 
	except KeyError as e: # No more results when next_results doesn't exist
		break
	# Create a dictionary from next_results, which has the following form:
	# ?max_id=847960489447628799&q=%23RIPSelena&count=100&include_entities=1 
	kwargs = dict([ kv.split('=') for kv in unquote(next_results[1:]).split("&") ])
	kwargs["tweet_mode"] = "extended"
	search_results = twitter_api.search.tweets(**kwargs)
	tweetsWriter(search_results['statuses'])

