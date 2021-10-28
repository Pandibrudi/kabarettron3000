import tweepy
import json
from scrt import constants

class TweetReader():

    def __init__(self):
        self.auth = tweepy.OAuthHandler(constants["API_KEY"], constants["API_KEY_SECRET"])
        self.auth.set_access_token(constants["ACCESS_TOKEN"], constants["ACCESS_TOKEN_SECRET"])
        self.api = tweepy.API(self.auth)
        print("Tweet Reader geladen!")

    def load_tweets(self):
        number_of_tweets = 200
        user_name = "dpa_live"
        tweets = self.api.user_timeline(screen_name=user_name, tweet_mode = "extended")

        tweet_dict = {}
        tweet_num = 0
        for t in tweets:
            tweet_num += 1
            t = t.full_text.replace("🟠 NEWSBLOG ", "").replace("+++", "").replace("🔵 UND SONST SO? ", "").replace("+ + +", "")
            tweet_dict[tweet_num] = t

        return tweet_dict
    
    def save_tweets(self):

        tweets_to_save = self.load_tweets()

        with open('data/data.json', 'w') as outfile:
            json.dump(tweets_to_save, outfile, indent=4, sort_keys=True)


if __name__ == "__main__":
    tr = TweetReader()
    tr.save_tweets()