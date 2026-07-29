from db.database import SessionLocal
from db.models import ContentItem, Source


def save_articles(articles):

    session = SessionLocal()

    saved = 0


    for item in articles:

        # Check duplicate article
        existing = (
            session.query(ContentItem)
            .filter(ContentItem.url == item["url"])
            .first()
        )


        if existing:
            continue


        # Create source for each RSS feed
        source = (
            session.query(Source)
            .filter(Source.url == item.get("source"))
            .first()
        )


        if not source:

            source = Source(
                name=item.get("source_name", "AI News RSS"),
                type="RSS",
                url=item.get("source", "unknown")
            )

            session.add(source)
            session.commit()
            session.refresh(source)



        article = ContentItem(

            source_id=source.id,

            title=item["title"],

            url=item["url"],

            raw_text=item.get(
                "summary",
                ""
            )

        )


        session.add(article)

        saved += 1


    session.commit()

    session.close()


    print(f"Saved {saved} articles")