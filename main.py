import os

import tweepy


# ツイート

api_key = os.environ["API_KEY"]
api_secret = os.environ["API_SECRET_KEY"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#media_ids = []

#res_media_ids = api.media_upload('data/today_finded.png')

#media_ids.append(res_media_ids.media_id)

api.update_status(status = 'test', )
