"""
Database Functions Module

This module provides database initialization, user management,
and helper functions for working with SQLAlchemy ORM models.

Features:
- Database connection setup with environment-based configuration.
- User registration and authentication with password hashing.
- Generic utility to fetch user fields from the database.
"""

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
    """
    Initialize the database schema.

    Creates all tables defined in SQLAlchemy models (if not already existing).

    Returns:
        None
    """
    Base.metadata.create_all(bind=engine)


def hash_password(password):
    """
    Generate a bcrypt hash for a given plaintext password.

    Args:
        password (str): User's plaintext password.

    Returns:
        str: Securely hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def register_user(db: Session, email, fullName, company, userType, password):
    """
    Register a new user in the database.

    Args:
        db (Session): SQLAlchemy session instance.
        email (str): User's email (unique identifier).
        fullName (str): User's full name.
        company (str): User's company.
        userType (str): Type of user (e.g., "admin", "client").
        password (str): Plaintext password.

    Returns:
        str: Status message:
             - "This email is already registered" if duplicate.
             - "Registration successful" if new user created.
    """
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        return 'This email is already registered'
    else:
        new_user = User(
            email=email,
            fullName=fullName,
            company=company,
            userType=userType,
            userRep=50.00,
            password=hash_password(password)
        )
        db.add(new_user)
        db.commit()
        return "Registration successful"


def logIn_success(db: Session, login, password):
    """
    Authenticate a user with email and password.

    Args:
        db (Session): SQLAlchemy session instance.
        login (str): User's email.
        password (str): Plaintext password.

    Returns:
        tuple:
            - (int, str): User ID and full name if authentication succeeds.
            - (None, None): If authentication fails.
    """
    user = db.query(User).filter(User.email == login).first()
    if user and bcrypt.checkpw(password.encode(), user.password.encode()):
        return user.id, user.fullName
    else:
        return None, None


def get_from_db(db: Session, user_id, *fields):
    """
    Fetch user data from the database.

    Args:
        db (Session): SQLAlchemy session instance.
        user_id (int): User's ID.
        *fields (str): Optional list of column names to fetch.
                       If empty, returns the full User object.

    Returns:
        - SQLAlchemy User object if no fields specified.
        - Single field value if one field requested.
        - Tuple of values if multiple fields requested.
        - None if user not found.
    """
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


def update_db(db: Session, user_id, data_dict):
    """
    Update fields of a user in the database. (Currently unimplemented)

    Args:
        db (Session): SQLAlchemy session instance.
        user_id (int): User's ID.
        data_dict (dict): Key-value pairs of fields to update.

    TODO:
        - Implement actual field updates.
    """
    for data in data_dict:
        pass
