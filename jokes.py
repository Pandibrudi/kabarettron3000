import json
import random
import spacy
import pyttsx3
from moviepy.editor import *
from datetime import datetime
from associations import get_associations
from joke_patterns import joke_patterns
from get_news import NewsReader

class Punchliner():

    def __init__(self):
        print("-- Kabaretttron3000 geladen! Happy joking!")
        pass
    
    def update_news(self):
        nr = NewsReader() 
        nr.save_news()

    def load_news(self):

        with open("data/news.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            random_news = data[str(random.randint(1, len(data)-1))]
        
        return random_news

    def get_news_topics(self, topic_num):
        headlines_and_topics = []
        for t in range(topic_num):
            headline = self.load_news()

            #look for the subject of the newsline to joke about it
            nlp = spacy.load("de_dep_news_trf")
            doc = nlp(headline)
            nouns =[]
            for token in doc:
                if token.pos_ == "NOUN":
                    nouns.append(token.text)
            
            topic = random.choice(nouns)
            headlines_and_topics.append((headline, topic))
        
        return headlines_and_topics

    def get_jokes(self, joke_type, joke_num): #aktuell: "buzzwords", "greetings", "setups", "punchlines", "transitions", "endings"
        joke_list = []
        joke_dict = joke_patterns[joke_type]
        
        try:
            joke_ids = random.sample(list(joke_dict), joke_num)
            for j in joke_ids:
                joke_list.append(joke_dict[j])
        except ValueError:
            joke_ids = random.sample(list(joke_dict), len(joke_dict))
            for j in joke_ids:
                joke_list.append(joke_dict[j])
            print("Value Error: Mehr Anfragen, als Jokes in der Datenbank. Naja dann werden Jokes halt wiederholt LOL \n")

        return joke_list

    def make_transition(self, old_topic, new_topic):

        transition_sample = random.choice(list(joke_patterns["transitions"].values()))
        transition = transition_sample
        transition = transition.replace("[OT]", old_topic).replace("[NT]", new_topic)
        
        return transition
    
    def make_greeting(self, city): # hier könnte man auch noch Namen usw. einbeziehen
        rnd_greeting = random.choice(list(joke_patterns["greetings"].values()))
        greeting = rnd_greeting.replace("[P]", city)
        rnd_punchline = random.choice(list(joke_patterns["punchlines"].values()))
        city_associations = get_associations(city)
        rnd_city_association = random.choice(city_associations)
        transition = self.make_transition(city, rnd_city_association)
        punchline = rnd_punchline.replace("[NN]", city).replace("[A]", rnd_city_association)
        greeting = greeting + " " + punchline + " " + transition + " "
        first_topic = rnd_city_association

        return greeting, first_topic

    
    def make_ending(self, city):# hier könnte man auch noch Namen usw. einbeziehen
        ending = random.choice(list(joke_patterns["endings"].values()))
        ending = ending.replace("[P]", city)

        return ending

    def make_comedy_set(self, city, name, topic_num, punchline_counter):
        comedy_set = ""
        setlist = self.get_news_topics(topic_num) #headlines + topic
        greeting = self.make_greeting(city)
        setups = self.get_jokes("setups", topic_num)
        punchlines = self.get_jokes("punchlines", punchline_counter * topic_num) 
        transistions = self.get_jokes("transitions", topic_num) 
        ending = self.make_ending(city)

        """print(f"Setlist: {setlist}")
        print(f"Begrüßung: {greeting}")
        print(f"Set Ups: {setups}")
        print(f"Punchlines: {punchlines}")
        print(f"Übergänge: {transistions}")
        print(f"Ende: {ending}")"""

        comedy_set = greeting[0] #weil es das erste ist

        parts = []
        topics = []
        final_transitions = []
        for headline in setlist:
            setup = random.choice(setups)
            setups.remove(setup)
            joke = setup + " " + headline[0]

            topic = headline[1]

            for i in range(punchline_counter):
                associations = get_associations(headline[1])
                punchline = random.choice(punchlines)
                punchlines.remove(punchline)
                punchline = punchline.replace("[NN]", headline[1])
                rnd_association = random.choice(associations)#wird nicht removed!
                punchline = punchline.replace("[A]", rnd_association)
                punchline = punchline.replace("[P]", city)
                punchline = punchline.replace("[N]", name)
                joke = joke + " " + punchline
            
            parts.append(joke)
            topics.append(topic)

        counter = 0
        for t in range(len(topics)-1):
            if counter != len(topics):
                transistion = random.choice(transistions)
                transistions.remove(transistion)
                transistion = transistion.replace("[OT]", topics[counter])
                transistion = transistion.replace("[NT]", topics[counter+1])
                counter = counter+1
                final_transitions.append(transistion)
            else:
                pass
        
        for p in range(len(parts)-1):
            comedy_set = comedy_set + " " + parts[p] + " " + final_transitions[p] + " "

        comedy_set = comedy_set + parts[-1]

        comedy_set = comedy_set + ending
        
        return comedy_set


    
    def make_audio(self, city, name, topic_num, punchline_counter):
        comedy_set = self.make_comedy_set(city, name, topic_num, punchline_counter)
        now = datetime.now()
        time = now.strftime("%d-%m-%Y_%H-%M-%S")
        file_name = "audio/joke_"+str(time)+".wav"

        engine = pyttsx3.init()
        engine.save_to_file(comedy_set, file_name)
        engine.runAndWait()

        return file_name, comedy_set

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
    print(pl.make_comedy_set("Hamburg", "Manfred", 3, 4))
    print("\n")
    

    