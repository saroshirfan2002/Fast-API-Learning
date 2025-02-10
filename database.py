from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db" ####sqlite:// → The first two slashes (//) are part of the URL scheme, similar to http://.
                                    ###/./test.db → The third slash (/) is the beginning of the file path.
                                    ###./test.db means the database is stored in the current directory (. means "current folder").
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) #If check_same_thread=False, multiple requests can work with the database at the same time.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() #This is the base class for all our database models. Any model we create will inherit from this class.