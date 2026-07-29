import re

from db.database import SessionLocal
from db.models import ContentItem

from collectors.article_scraper import extract_article_text
from services.summarizer import summarize_article


session = SessionLocal()


articles = (
    session.query(ContentItem)
    .filter(ContentItem.summary == None)
    .all()
)


print(f"Found {len(articles)} articles to summarize.")



for article in articles:


    print("\nProcessing:")
    print(article.title)


    text = extract_article_text(article.url)


    output = summarize_article(text)


    print(output)


    summary_match = re.search(
        r"SUMMARY:\s*(.*?)\s*CATEGORY:",
        output,
        re.S
    )


    category_match = re.search(
        r"CATEGORY:\s*(.*)",
        output,
        re.S
    )


    if summary_match:

        article.summary = summary_match.group(1).strip()


    if category_match:

        article.category = category_match.group(1).strip()



    session.commit()



session.close()


print("DONE")