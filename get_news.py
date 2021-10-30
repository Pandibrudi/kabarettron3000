import json
import feedparser

class NewsReader():

    def __init__(self):
        self.news = feedparser.parse("https://www.tagesschau.de/xml/rss2/")

    def save_news(self):
        self.news_dict = {}

        for i in range(len(self.news)):
            self.news_dict[i] = self.news.entries[i]["title"]

        with open("data/news.json", "w", encoding="utf-8") as outfile:
            json.dump(self.news_dict, outfile, indent=4, sort_keys=True, ensure_ascii=False)
        
        return self.news_dict

if __name__ == "__main__":
    nr = NewsReader()
    nr.save_news()



