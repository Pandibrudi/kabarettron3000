import twitter
from scrt import constants

class TweetReader():

    def __init__(self):
        api = twitter.Api(consumer_key=constants["API_KEY"],
                          consumer_secret=constants["API_KEY_SECRET"],
                          access_token_key=constants["ACCESS_TOKEN"],
                          access_token_secret=constants["ACCESS_TOKEN_SECRET"])
        print("Tweet Reader geladen!")

    def load_tweets(self):
        print("lol")


if __name__ == "__main__":
    tr = TweetReader()
    tr.load_tweets()