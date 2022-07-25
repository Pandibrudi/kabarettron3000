import json
import random
import spacy
import pyttsx3
from moviepy.editor import *
from datetime import datetime
from associations import get_associations
from joke_patterns import setups, punchlines, greetings, transitions, endings
from get_news import NewsReader

class Punchliner():

    def __init__(self):
        #evtl hier die punchlines sammeln, sodass sich das programm es aus 
        #einer instanzierten Version der Tabelle zieht und samples nehmen kann
        # self.topic_length 
        # self.num_topics
        # Diese Werte müssten dazu vordefiniert werden sobald die Klasse aufgerufen wird
        # dann lässt sich errechnen wie groß die Sample der einzelnen Patterns sein müssen
        pass
    
    def update_news(self):
        nr = NewsReader() 
        nr.save_news()

    def get_news(self):

        with open("data/news.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            random_news = data[str(random.randint(1, len(data)-1))]
        
        return random_news
    
    def make_joke_from_news(self, lines):

        news = self.get_news()

        #look for the subject of the newsline to joke about it
        nlp = spacy.load("de_dep_news_trf")
        doc = nlp(news)
        nouns =[]
        for token in doc:
            if token.pos_ == "NOUN":
                nouns.append(token.text)
        
        joke_object = random.choice(nouns)
        joke_object_associations = get_associations(joke_object)

        joke_setup = setups[random.randint(1, len(setups)-1)]

        punchline_counter = lines
        punchline_sample = random.sample(list(punchlines), punchline_counter)

        joke_from_news = joke_setup + " " + news

        for i in range(punchline_counter):
            rnd_association = random.choice(joke_object_associations)
            joke_from_news = joke_from_news + " " + punchlines[punchline_sample[i]].replace("[NN]", joke_object).replace("[A]", rnd_association) + " "

        return joke_from_news, joke_object
    

    def make_joke_from_topic(self, lines, topic):
        joke = ""
        topic_associations = get_associations(topic)
        punchline_counter = lines
        punchline_sample = random.sample(list(punchlines), punchline_counter)

        for i in range(punchline_counter):
            rnd_association = random.choice(topic_associations)
            joke = joke + " " + punchlines[punchline_sample[i]].replace("[NN]", topic).replace("[A]", rnd_association) + " "

        return joke
    
    def make_transition(self, old_topic, new_topic):
        transition_sample = random.choice(list(transitions.values()))
        transition = transition_sample
        transition = transition.replace("[OT]", old_topic).replace("[NT]", new_topic)
        
        return transition

    def make_comedy_set(self, city, num_topics):
        greeting = greetings[random.randint(1, len(greetings)-1)]
        greeting = greeting.replace("[P]", city)

        city_associations = get_associations(city)
        rnd_city_association = random.choice(city_associations)

        transition_entry = self.make_transition(city, rnd_city_association)

        city_joke = self.make_joke_from_topic(5, rnd_city_association)

        ending = random.choice(list(endings.values()))
        ending = ending.replace("[P]", city)

        jokes = ""     

        for i in range(num_topics):
            #kann auch variiert werden oder zufallsbasiert sein, wie lang ein Thema abgehandelt wird
            #könnte im GUI dann eingestellt werden
            news_joke_and_topic = self.make_joke_from_news(5) 
            news_joke = news_joke_and_topic[0]
            news_associations = get_associations(news_joke_and_topic[1])
            rnd_news_association = random.choice(news_associations)
            news_transition = self.make_transition(news_joke_and_topic[1], rnd_news_association)
            topic_joke = self.make_joke_from_topic(5, rnd_news_association)
            jokes = jokes + "\n" + news_joke + " " + news_transition + " " + topic_joke + " "

        comedy_set = greeting + " " + transition_entry + " " + city_joke + " " + jokes + ending

        print(comedy_set)
        return comedy_set

    
    def make_audio(self, city, topics):
        joke = self.make_comedy_set(city, topics)
        now = datetime.now()
        time = now.strftime("%d-%m-%Y_%H-%M-%S")
        file_name = "audio/joke_"+str(time)+".wav"

        engine = pyttsx3.init()
        engine.save_to_file(joke, file_name)
        engine.runAndWait()

        return file_name, joke

    def make_video(self, city):
        audio_file = self.make_audio(city)
        audioclip = AudioFileClip(audio_file)
        new_audioclip = CompositeAudioClip([audioclip])

        img = ['img/bot_img.jpg']
        clips = [ImageClip(m).set_duration(new_audioclip.duration) for m in img] #weg finden die Dauer des Clips auf die Dauer der Audio zu setzen
        concat_clip = concatenate_videoclips(clips, method="compose")
        concat_clip.write_videofile("video/bot_video.mp4", fps=24)
        videoclip = VideoFileClip("video/bot_video.mp4")
        videoclip.audio = new_audioclip

        now = datetime.now()
        time = now.strftime("%d-%m-%Y_%H-%M-%S")
        filename = f"video/comedyclip_{time}.mp4"
        videoclip.write_videofile(filename, verbose=True, codec="libx264")

if __name__ == "__main__":
    pl = Punchliner()
    print("\n")
    #pl.make_audio("Hamburg")
    #pl.make_comedy_set("Hamburg")
    #pl.make_joke_from_topic(10, "Hühner")
    print("\n")