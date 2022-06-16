import spacy
import random
import wikipediaapi
from base64 import decode
import requests, json
from joke_patterns import buzzwords



def get_associations(word):

    associations = []
    
    try:
        #Wikipedia Part
        wiki_wiki = wikipediaapi.Wikipedia('de')

        page_py = wiki_wiki.page(word)

        #print("Page - Summary: %s" % page_py.summary)

        nlp = spacy.load("de_dep_news_trf")
        doc = nlp(page_py.summary) #vielleicht mehr als nur das wiki summary
        for token in doc:
            if token.pos_ == "NOUN":
                if token.pos_ not in associations:
                    if len(token.text) > 2:
                        associations.append(token.text.replace("Siehe",""))
        

        #Google Part
        URL="http://suggestqueries.google.com/complete/search?client=firefox&q="+word

        response = requests.get(URL, {'User-agent':'Mozilla/5.0'})

        ergebnis = json.loads(response.content.decode("ISO-8859-1"))

        ergebnis = ergebnis[1]

        for w in ergebnis:
            if len(word) > 3:
                associations.append(w.strip(" "))
        
        associations = list(dict.fromkeys(associations)) #remove duplicates

    except:
        print("Error while getting Wikipedia and Google!")
        rnd_buzzword = random.choice(list(buzzwords.values()))
        associations.append(rnd_buzzword)
    
    if len(associations) == 0:
        print(f"No Associations found for {word}.")
        rnd_buzzword = random.choice(list(buzzwords.values()))
        associations.append(rnd_buzzword)
    
    return associations