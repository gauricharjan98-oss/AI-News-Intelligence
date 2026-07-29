from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from db.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    type = Column(String, nullable=False)

    url = Column(String, unique=True)

    active = Column(Boolean, default=True)

    last_checked = Column(DateTime)

    content_items = relationship(
        "ContentItem",
        back_populates="source"
    )


class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(Integer, primary_key=True)

    source_id = Column(Integer, ForeignKey("sources.id"))

    title = Column(String, nullable=False)

    url = Column(String, unique=True)

    published_at = Column(DateTime)

    raw_text = Column(Text)

    clean_text = Column(Text)

    summary = Column(Text)

    category = Column(String)

    digest_id = Column(Integer, ForeignKey("digests.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    source = relationship(
        "Source",
        back_populates="content_items"
    )

    digest = relationship(
        "Digest",
        back_populates="content_items"
    )


class Digest(Base):
    __tablename__ = "digests"

    id = Column(Integer, primary_key=True)

    date = Column(DateTime, default=datetime.utcnow)

    title = Column(String)

    generated_summary = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    content_items = relationship(
        "ContentItem",
        back_populates="digest"
    )