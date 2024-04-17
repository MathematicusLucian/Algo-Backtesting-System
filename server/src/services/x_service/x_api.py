import tweepy
import csv
import datetime
import pandas as pd
from src.utils import get_envar

class XService(tweepy.StreamingClient):
    def __init__(self):
        self.limit = 1

    def _get_auth_full(self):
        consumer_token = get_envar('X_CONSUMER_TOKEN')
        consumer_token_secret = get_envar('X_CONSUMER_TOKEN_SECRET')
        access_token = get_envar('X_ACCESS_TOKEN')
        access_token_secret = get_envar('X_ACCESS_TOKEN_SECRET')
        return consumer_token, consumer_token_secret, access_token, access_token_secret

    def _get_bearer_token(self) -> str:
        return get_envar('X_BEARER_TOKEN')
    
    def _x_bearer_client_setup(self):
        return tweepy.Client(self._get_bearer_token())

    def _x_api_setup(self):
        consumer_token, consumer_token_secret, access_token, access_token_secret = self._get_auth_full()
        auth = tweepy.OAuthHandler(consumer_token, consumer_token_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

    def get_status_details(self, status):
        return status.user.screen_name + ": " + status.text
       
    def fetch_tweets(self, handle):
        x_api = self._x_api_setup()
        print(x_api.get_me()) 
        # new_tweets = x_api.user_timeline(screen_name=handle, count=self.limit)
        # print(new_tweets)
        # labels = [["link", "username" "tweet"]]
        # currentime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # self.print_tweets(handle, responses, labels, currentime)

    def disconnect_if_limit(self, tweets):
        if len(tweets) == self.limit:
            self.disconnect()
    
    def print_tweets(self, handle, responses, labels, currentime):
        counter = 0
        for response in responses:
            counter += 1
            try:
                for tweet in response.data:
                    labels.append([f"https://twitter.com/{handle}/status/{tweet.id}", handle, tweet.text])
            except Exception as e:
                print(e)
        # columns = ['User', 'Tweet']
        # data = []
        # for tweet in tweets:
        #     data.append([tweet.user.screen_name, tweet.full_text])
        # df = pd.DataFrame(data, columns=columns)
        # print(df)
        with open(f"tweets_{handle}_{currentime}.csv", "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(labels)