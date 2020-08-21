import datetime
import requests, bs4

SECOND = 1
MINUTE = 60*SECOND
HOUR = 60*MINUTE
TZ = 3*HOUR

def check_tweet_by_id(link):
    response = requests.get('https://twitter.com'+link)
    html_code = response.text
    return 'Sorry, that page doesn’t exist!' not in html_code



def mine_tweet(tweet):
    tweet_link = tweet.find('div', {'class': 'js-stream-tweet'})['data-permalink-path']
    tweet_id = tweet['data-item-id']
    tweet_text = tweet.find('div', {'class': 'js-tweet-text-container'}).text
    tweet_timestamp = datetime.datetime.fromtimestamp(int(tweet.find('span', {'class': 'js-short-timestamp'})['data-time'])+TZ)
    tweet_replies = int(tweet.find('span', {'class': 'ProfileTweet-action--reply'}).find('span', {'class': 'ProfileTweet-actionCount'})['data-tweet-stat-count'])
    tweet_retweets = int(tweet.find('span', {'class': 'ProfileTweet-action--retweet'}).find('span', {'class': 'ProfileTweet-actionCount'})['data-tweet-stat-count'])
    tweet_favorites = int(tweet.find('span', {'class': 'ProfileTweet-action--favorite'}).find('span', {'class': 'ProfileTweet-actionCount'})['data-tweet-stat-count'])
    return [check_tweet_by_id(tweet_link), tweet_id, tweet_link, tweet_timestamp, tweet_text, tweet_replies, tweet_retweets, tweet_favorites]


fn = 'html/CarlosBolsonaro/2020_05_01_23_39.html'
fh = open(fn)
html_code = fh.read()
fh.close()
soup = bs4.BeautifulSoup(html_code, 'html.parser')
# tweets = soup.findAll('div', {'class': 'js-tweet-text-container'})
tweets = soup.findAll('li', {'class': 'js-stream-item'})
print(len(tweets))
for tweet in tweets:
    # [tweet_timestamp, tweet_text, tweet_replies, tweet_retweets, tweet_favorites] = mine_tweet(tweet)
    # print([tweet_timestamp, tweet_text, tweet_replies, tweet_retweets, tweet_favorites])
    print(mine_tweet(tweet), '\n\n')