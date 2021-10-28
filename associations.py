import json
import random
import spacy
from get_tweets import TweetReader

class Punchliner():

    def __init__(self):
        tr = TweetReader() #get new tweets and save it at data/data.json

    def get_setup(self):

        with open("data/data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            random_tweet = data[str(random.randint(1, len(data)))]
        
        return random_tweet
    
    def make_joke(self):

        setup = self.get_setup()

        #look for the subject of the tweet to joke about it
        nlp = spacy.load("de_dep_news_trf")
        doc = nlp(setup)
        
        for token in doc:
            if token.dep_ == "nsubj":
                joke_object = token.text
                print(joke_object)

        print(f"Habt ihr schon gehört?! {setup}")
        #print(f"Witz über {joke_object}")



if __name__ == "__main__":
    pl = Punchliner()
    pl.make_joke()