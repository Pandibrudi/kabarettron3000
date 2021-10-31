import json
import random
import spacy
import pyttsx3
from moviepy.editor import *
from datetime import datetime
from joke_patterns import setups, punchlines
from get_news import NewsReader

class Punchliner():

    def __init__(self):
        #tr = TweetReader() #old approach
        nr = NewsReader() #new
        nr.save_news()

    def get_news(self):

        with open("data/news.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            random_news = data[str(random.randint(1, len(data)-1))]
        
        return random_news
    
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

        joke_setup = setups[random.randint(1, len(setups)-1)]

        punchline_counter = 3
        punchline_sample = random.sample(list(punchlines), punchline_counter)

        joke = joke_setup + " " + news

        for i in range(punchline_counter):
            joke = joke + " " + punchlines[punchline_sample[i]].replace("[NN]", joke_object) + " "
        
        print(joke)

        return joke
    
    def make_audio(self):
        joke = self.make_joke()
        now = datetime.now()
        time = now.strftime("%d-%m-%Y_%H-%M-%S")
        file_name = "audio/joke_"+str(time)+".mp3"

        engine = pyttsx3.init()
        engine.save_to_file(joke, file_name)
        engine.runAndWait()

        return file_name

    def make_video(self):
        img = ['img/bot_img.jpg']
        clips = [ImageClip(m).set_duration(30) for m in img] #weg finden die Dauer des Clips auf die Dauer der Audio zu setzen
        concat_clip = concatenate_videoclips(clips, method="compose")
        concat_clip.write_videofile("video/bot_video.mp4", fps=24)

        audio_file = self.make_audio()
        videoclip = VideoFileClip("video/bot_video.mp4")
        audioclip = AudioFileClip(audio_file)
        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip

        now = datetime.now()
        time = now.strftime("%d-%m-%Y_%H-%M-%S")
        filename = f"video/comedyclip_{time}.mp4"
        videoclip.write_videofile(filename)

        

if __name__ == "__main__":
    pl = Punchliner()
    print("\n")
    pl.make_audio()
    pl.make_video()
    print("\n")