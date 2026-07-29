from collectors.blog_rss import fetch_articles
from services.save_articles import save_article


def clean_article(item):
    """
    Convert RSS object into our database format
    """

    article = {
        "title": item.get("title", "No Title"),
        "url": item.get("link", ""),
        "summary": item.get("summary", "")
    }

    return article


def run_collector():

    print("Starting News Collector...")

    articles = fetch_articles()

    print("\nTotal articles fetched:", len(articles))


    for item in articles:

        article = clean_article(item)

        save_article(article)


    print("\nCollector Finished Successfully!")


if __name__ == "__main__":
    run_collector()