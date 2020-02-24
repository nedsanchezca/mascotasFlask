# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 09:47:23 2020

@hor: Gabriela
"""

import tweepy
import json
import csv

#Autenticacion a la API de twitter
api_key = "J7goYmTliL5SN6JxNBcTnaV9P"
api_secret_key = "mECQnrsacSIHIlWYBW8NlkQQKiqMKO5WBtFQQZWJIitfauOvPP"
access_token = "870273825769959424-r85QoXzCVHpNk03vOyqP2FikIj6F9uA"
access_token_secret = "uqOBdmbCYhXyIwjllSZmu5nmlMl2yNn9xL9u086TF6tG0"

aut = tweepy.OAuthHandler(api_key, api_secret_key)
aut.set_access_token(access_token, access_token_secret)

api = tweepy.API(aut, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

csvFile = open('result.csv', 'a')
csvWriter = csv.writer(csvFile)

tweetsMascotas = tweepy.Cursor(api.search,
                   q = "mascotas",
                   since='2018-04-23').items(1000)

for tweet in tweetsMascotas:
    csvWriter.writerow([tweet.created_at, tweet.text, tweet.favorite_count, tweet.retweet_count, len(tweet.text)])
    print(tweet.created_at, tweet.text) 

csvFile.close()