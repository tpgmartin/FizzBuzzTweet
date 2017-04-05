import random
import re
import requests
import tweepy
from secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

def tweet_number(number, username, status_id):
  result = ' '.join(fizz_buzz(number))
  tweet = '{0} @{1}'.format(result, username)
  api.update_status(tweet, in_reply_to_status_id=status_id)

def fizz_buzz(numbers):
  output = []

  for n in numbers:
    n = int(n)
    fizz = lambda x: 'Fizz' if x%3==0 else str()
    buzz = lambda x: 'Buzz' if x%5==0 else str()
    output.append(fizz(n) + buzz(n) or str(n))
  
  return output


class BotStreamer(tweepy.StreamListener):
    def on_status(self, status):
        username = status.user.screen_name
        text = status.text
        status_id = status.id

        numbers = re.findall(r'\d+', text)
        if (numbers):
          tweet_number(numbers, username, status_id)
        else:
          api.update_status('Please tweet some numbers @{0}'.format(username), in_reply_to_status_id=status_id)

myStreamListener = BotStreamer()

stream = tweepy.Stream(auth, myStreamListener)
stream.filter(track=['@FizzBuzzTweet'])