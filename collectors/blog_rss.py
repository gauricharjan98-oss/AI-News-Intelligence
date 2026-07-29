from services.save_articles import save_articles

import feedparser
import yaml
from pathlib import Path



def load_sources():

    path = Path("config/sources.yaml")

    print("Loading sources from:", path.resolve())


    with open(path, "r", encoding="utf-8") as file:

        data = yaml.safe_load(file)


    print("Loaded sources raw:", data)


    if "blogs" not in data:

        raise KeyError("Missing blogs key")


    return data



def fetch_articles():

    sources = load_sources()

    articles = []


    for url in sources["blogs"]:

        print("\nChecking:", url)


        feed = feedparser.parse(url)


        print("Number of items found:", len(feed.entries))


        for item in feed.entries[:5]:


            print("\nARTICLE FOUND")

            print(item.title)



            articles.append({

                "title": item.get(
                    "title",
                    "No title"
                ),


                "url": item.get(
                    "link",
                    ""
                ),


                "summary": item.get(
                    "summary",
                    ""
                ),


                "source": url,


                "source_name": feed.feed.get(
                    "title",
                    "AI RSS Source"
                )

            })


    return articles





if __name__ == "__main__":


    articles = fetch_articles()


    print("\n===================")

    print("TOTAL ARTICLES:", len(articles))

    print("===================")



    save_articles(articles)