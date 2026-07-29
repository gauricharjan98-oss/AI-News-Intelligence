from datetime import datetime
from pathlib import Path

from db.database import SessionLocal
from db.models import ContentItem


def generate_digest():
    session = SessionLocal()

    articles = (
        session.query(ContentItem)
        .filter(ContentItem.summary != None)
        .order_by(ContentItem.published_at.desc())
        .all()
    )

    print(f"Found {len(articles)} summarized articles.")

    today = datetime.now().strftime("%Y-%m-%d")

    digest = f"# AI News Daily Digest ({today})\n\n"

    for article in articles:
        digest += f"## {article.title}\n\n"
        digest += f"**Category:** {article.category}\n\n"
        digest += f"{article.summary}\n\n"

        if article.url:
            digest += f"Read More: {article.url}\n\n"

        digest += "---\n\n"

    output = Path("daily_digest.md")
    output.write_text(digest, encoding="utf-8")

    print(f"✅ Digest saved to {output.resolve()}")

    session.close()


if __name__ == "__main__":
    generate_digest()