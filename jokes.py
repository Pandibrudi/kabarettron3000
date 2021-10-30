import json
import random
import spacy
import pyttsx3
from joke_patterns import setups, punchlines
from get_news import NewsReader

class Punchliner():

    def __init__(self):
        #tr = TweetReader() #old approach
        nr = NewsReader() #new
    def get_news(self):

        with open("data/news.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            random_tweet = data[str(random.randint(1, len(data)))]
        
        return random_tweet
    
    def make_joke(self):

        news = self.get_news()

        #look for the subject of the tweet to joke about it
        nlp = spacy.load("de_dep_news_trf")
        doc = nlp(news)
        nouns =[]
        for token in doc:
            if token.pos_ == "NOUN":
                nouns.append(token.text)
        
        joke_object = random.choice(nouns)

        joke_setup = setups[random.randint(1, len(setups))]

        punchline_counter = 3
        punchline_sample = random.sample(list(punchlines), punchline_counter)

        joke = joke_setup + news

        for i in range(punchline_counter):
            joke = joke + " " + punchlines[punchline_sample[i]].replace("[NN]", joke_object) + " "

        return joke
    
    def make_audio(self):
        joke = self.make_joke()
        engine = pyttsx3.init()
        engine.save_to_file(joke, 'audio/joke.mp3')
        engine.runAndWait()
        

if __name__ == "__main__":
    pl = Punchliner()
    print("\n")
    print(pl.make_audio())
    print("\n")