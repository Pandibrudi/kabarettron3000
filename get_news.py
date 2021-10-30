import json
import feedparser

class NewsReader():

    def __init__(self):
        self.urls = ["https://newsfeed.zeit.de/index",
                      "https://www.tagesschau.de/xml/rss2/"
                     ]

        self.feeds = []
        self.news = []

        for url in self.urls:
            self.feeds.append(feedparser.parse(url))

        for feed in self.feeds:
            for post in feed.entries:
                self.news.append(post.title)

    def save_news(self):
        self.news_dict = {}

        for i in range(len(self.news)):
            self.news_dict[i] = self.news[i]+"."

        with open("data/news.json", "w", encoding="utf-8") as outfile:
            json.dump(self.news_dict, outfile, indent=4, sort_keys=True, ensure_ascii=False)
        
        return self.news_dict

if __name__ == "__main__":
    nr = NewsReader()
    nr.save_news()



