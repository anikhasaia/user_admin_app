import os

from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import User

load_dotenv()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def create_admin():
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")

    existing_user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if existing_user is None:
        hashed_password = pwd_context.hash(password)

        admin = User(
            username=username,
            password=hashed_password,
            role="admin"
        )

        db.add(admin)
        db.commit()

        print(f"Admin user '{username}' created.")
    else:
        print(f"Admin user '{username}' already exists.")

    db.close()