import json
import random
import spacy
from joke_patterns import setups, punchlines
from get_tweets import TweetReader

class Punchliner():

    def __init__(self):
        tr = TweetReader() #get new tweets and save it at data/data.json

    def get_news(self):

        with open("data/data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            random_tweet = data[str(random.randint(1, len(data)))]
        
        return random_tweet
    
    def make_joke(self):

        news = self.get_news()

        #look for the subject of the tweet to joke about it
        nlp = spacy.load("de_dep_news_trf")
        doc = nlp(setup)
        nouns =[]
        for token in doc:
            if token.pos_ == "NOUN":
                nouns.append(token.text)
        
        joke_object = random.choice(nouns)

        joke_setup = setups[random.randint(1, len(setups))]
        joke_punchline = punchlines[random.randint(1, len(setups))]

        joke = joke_setup + news + joke_punchline

        return joke



if __name__ == "__main__":
    pl = Punchliner()
    pl.make_joke()