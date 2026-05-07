from fastapi import FastAPI
from uuid import UUID,  uuid4
from pydantic import BaseModel, Field



app=FastAPI()
# starting doing a todo application backend!!

class BaseOut(BaseModel):
    msg : str
    error : str=False

class Todo(BaseModel):
    id: UUID =Field(default_factory=uuid4)
    name : str
    category :  str
    status : bool

# local variable for todo
db: list[Todo] =[]

class TodoCreateOut(BaseOut):
    todo : Todo

@app.post(
    "/create",
    response_model=TodoCreateOut
)

def create_todo(todo:Todo) ->TodoCreateOut:
    db.append(todo)
    return TodoCreateOut(todo=Todo,msg="successfully created::")

class TodoGetOut(BaseOut):
    todos: list[Todo]


@app.get("/todos")
def fetch_todos():
    return TodoGetOut(todos=db,msg="todos haru fetch vayo::")

