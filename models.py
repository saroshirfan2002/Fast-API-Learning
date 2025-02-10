from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) #Speeds up searches when filtering users by id
    name = Column(String, index=True) #index= true means Helps with faster lookups when using name
    email = Column(String, unique=True, index=True)
    password = Column(String)
