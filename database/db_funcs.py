from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from model.dbModels import Base, User
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def register_user(db: Session, email, fullName, company, password):
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        return 'This email is already registered'
    else:
        new_user = User(
            email=email,
            fullName=fullName,
            company=company,
            password=hash_password(password)
        )
        db.add(new_user)
        db.commit()
        return "Registration successful"


def logIn_success(db: Session, login, password):
    user = db.query(User).filter(User.email == login).first()
    if user and bcrypt.checkpw(password.encode(), user.password.encode()):
        return user.id, user.fullName
    else:
        return None


def get_from_db(db: Session, user_id, *fields):
    if not fields:
        user = db.query(User).filter(User.id == user_id).first()
        return user

    allowed_fields = set(c.name for c in User.__table__.columns)
    selected_fields = [f for f in fields if f in allowed_fields]

    if not selected_fields:
        user = db.query(User).filter(User.id == user_id).first()
        return user

    columns = [getattr(User, f) for f in selected_fields]
    result = db.query(*columns).filter(User.id == user_id).first()

    if result is None:
        return result

    if len(selected_fields) == 1:
        return result[0]
    else:
        return tuple(result)
