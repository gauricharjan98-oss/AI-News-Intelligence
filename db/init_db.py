from db.database import engine, Base
from db import models

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database created successfully!")