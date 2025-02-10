from fastapi import FastAPI, HTTPException, Depends
from basemodel import User, UserResponse, UserWithPassword
from fastapi import status    #for using http status responses e.g 202,402, 404, 200 etc
from sqlalchemy.orm import Session
from database import SessionLocal  # Import the database session and This is the session that connects to the database.
from crud import create_user, get_user_by_name, get_users  # Import CRUD operations
import httpx
import asyncio
from database import engine, Base
import models 
from typing import List

app = FastAPI()

# This function creates a database session and yields it for use in your routes. After the request is completed, the session is closed to release resources
def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Provide the session to any route that depends on it
    finally:
        db.close()  # Close the session when done and release resoucres


@app.get("/")
def home():
    return {"message": "Hello, my name is Sarosh!"}

@app.get("/about")
def about_me():
    return {"name": "Sarosh!", 
            "age" : "22"}

@app.get("/user/{user_id}")  #path parameters is inserted directly in the url
#       /user/5 should return details for user 5
def get_user(user_id:int ):
    
    return {"user_id": user_id, "message": "User details fetched!"}

@app.get("/search")  #query parameters, giving them is sometimes optional in url
def search(name:str, user_id :int, age:int = None ):
    #return({"user_id ": user_id, "age" : age, "name ": name})
    return {"message": f"Searching for {name}, Age {age}"}

#For POST requests, we send data in the request body instead of the URL.
#FastAPI uses Pydantic models to validate and enforce data structure.
@app.post("/user/", response_model=User, status_code=status.HTTP_200_OK)
def create_user(user: User):

    if user.age < 18:
        raise HTTPException(status_code=400, detail="User must be at least 18 years old.")
    return user #whatever mentioned in response model, only can send that

#Create a new route /calculate that accepts two numbers as query parameters and returns their sum
#Example: URL: /calculate?num1=10&num2=5

@app.get("/calculate")

def calculate( num1:int, num2:int):
    sum = num1 + num2
    return{"sum":sum }

@app.post("/user_response_model/", response_model=UserResponse)
def create_user(user: UserWithPassword):
    return {"message": "User created!", "user": user.dict(exclude={"admin"})}
'''
@app.get("/fetch-data")
async def fetch_todo():
    async with httpx.AsyncClient() as client: #async with ensures that the connection closes properly after the request completes.
        response = await client.get("https://jsonplaceholder.typicode.com/todos/1") #await tells Python: "Do not block the execution. Just wait for the response and continue."
        return response.json()

async def fetch_user():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/users/1")
        return response.json()

@app.get("/fetch-multiple")
async def fetch_multiple():
    todo, user = await asyncio.gather(fetch_todo(), fetch_user())
    return {"todo": todo, "user": user}'''

# Create database tables
Base.metadata.create_all(bind=engine)  ## Creates all the tables defined in our models.py file.
                                       ##If a table does not exist, it will be created automatically.
                                        ##If the table already exists, nothing happens (it won’t overwrite existing data).

@app.get("/user/", response_model=UserResponse)
def get_user_by_name_route(name: str, db: Session = Depends(get_db)):
    db_user = get_user_by_name(db=db, u_name=name) #passed to crud operation
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User details fetched successfully", "user": db_user}

@app.post("/user/", response_model=User, status_code=status.HTTP_200_OK)
def create_new_user(user: User, db: Session = Depends(get_db)):  # Use Depends to get db session
    if user.age < 18:
        raise HTTPException(status_code=400, detail="User must be at least 18 years old.")
    return create_user(db=db, user=user)  # Call create_user from crud.py


@app.get("/all_users/", response_model=List[User])
def get_all_users_routes(db: Session = Depends(get_db)):
    users = get_users(db=db, skip=0, limit=10)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users  
