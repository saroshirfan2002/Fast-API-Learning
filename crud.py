#we define functions that interact with the database to perform CRUD (Create, Read, Update, Delete) operations on the User table.
from sqlalchemy.orm import Session
from models import User
from basemodel import UserCreate  # Pydantic model for request validation

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email, password=user.password)  # Create a new user instance
    db.add(db_user)  # Add the user to the session (but not committed yet)
    db.commit()  # Commit the transaction (this will insert the user into the database) 
    db.refresh(db_user)  # Refresh the user object with data from the database (including the new `id`)
    return db_user  # Return the created user object

def get_users(db: Session, skip: int = 0, limit: int = 10):
    # Fetch a list of users from the database, with optional pagination (skip and limit)
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_name(db: Session, u_name: str):
    # Fetch a user by their name
    return db.query(User).filter(User.name == u_name).first()  # `first()` returns the first match or None if not found

def delete_user(db: Session, user_id: int):
    # Find the user by ID
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:  # If user exists, delete them
        db.delete(db_user)
        db.commit()  # Commit the deletion to the database
    return db_user  # Return the deleted user (or None if not found)
