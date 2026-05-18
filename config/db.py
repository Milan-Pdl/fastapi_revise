#store the information of database structure like tables, columns, relationships, etc. I
# It is used by SQLAlchemy to manage the database schema and perform operations on the database.
from sqlalchemy import MetaData

#asyncio is a library for writing concurrent code using the async/await syntax. 
# It provides a way to write asynchronous code that can run concurrently, allowing for better performance and 
# responsiveness in applications that involve I/O operations, such as database interactions.

#AsyncSession is a class provided by SQLAlchemy that represents an asynchronous session for interacting with the database. 
# It allows you to perform database operations asynchronously, which can improve the performance of your application by
# allowing other tasks to run while waiting for database operations to complete.

#create_async_engine is a function provided by SQLAlchemy that creates an asynchronous engine for connecting to the database. 
# It is used to establish a connection to the database and manage the connection pool for asynchronous operations

#async_sessionmaker is a function provided by SQLAlchemy that creates an asynchronous session factory. 
# It is used to create instances of AsyncSession that can be used to interact with the database asynchronously.
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker

#declarative_base is a function provided by SQLAlchemy that creates a base class for declarative models. 
# It is used to define the structure of the database tables and their relationships in a declarative

from sqlalchemy.orm import declarative_base

#connecttion string
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost/todo_db"

DEFAULT_SCHEMA_NAME="TODO_S"

# create the table with the name of TODO_S
metadata=MetaData(schema=DEFAULT_SCHEMA_NAME)



#parent class for all the models
class Base(declarative_base):
    metadata = metadata

engine = create_async_engine(DATABASE_URL,
                              echo=True,
                              )

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False) 

#get_db is a function that provides a database session for use in the application. I
# It is defined as an asynchronous generator function that yields an instance of AsyncSession. 
# This allows the application to use the database session in an asynchronous context, 
# enabling efficient handling of database operations without blocking the main thread of execution.

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


