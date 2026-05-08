from fastapi import FastAPI,APIRouter
from uuid import UUID,  uuid4
from pydantic import BaseModel, Field



app=FastAPI()
# starting doing a todo application backend!!

get_router=APIRouter(prefix="/get",tags=["Get route"])
post_router=APIRouter(prefix="/post",tags=["post route"])
delete_router=APIRouter(prefix="/delete",tags=["delete route"])
update_router=APIRouter(prefix="/put",tags=["update route"])

class BaseOut(BaseModel):
    msg : str
    error : str=False

class Todo(BaseModel):
    id: UUID =Field(default_factory=uuid4)
    name : str
    category :  str
    status : bool= False

# local variable for todo
db: list[Todo] =[]


class TodoCreateOut(BaseOut):
    todo : Todo

@post_router.post(
    "/create",
    response_model=TodoCreateOut
)
def create_todo(todo:Todo) ->TodoCreateOut:
    db.append(todo)
    return TodoCreateOut(todo=todo,msg="successfully created::")

class TodoGetOut(BaseOut):
    todos: list[Todo]


@get_router.get(
        "/todos",
        response_model=TodoGetOut
)

def fetch_todos():
    return TodoGetOut(todos=db,msg="todos haru fetch vayo::")

# print(db[0])

# fetch todo by id
@get_router.get(
    "/todo/{user_id}",
    response_model=TodoCreateOut | BaseOut
)

def fetchTodos_by_id(user_id:str) -> TodoCreateOut | BaseOut:
    try:
        user_id=UUID(user_id)
    except Exception as ex:
        return BaseOut(msg="Invalied uuid",error=str(ex))
    
    for todo in db:
        if todo.id==user_id:
            return TodoCreateOut(todo=todo,msg=f"todo is fetched for id {user_id}")
    return BaseOut(msg="no to do found::")

# updating the name of a todoapp
# @update_router.put(
#     "/update_name/{user_id}",
#     response_model= TodoCreateOut
#     )

class UpdateName(BaseModel):
    name: str


# updating yo do as peer the username
@update_router.put("/todo/{user_id}")
def update_name(user_id: str, updatePost: UpdateName):

    try:
        user_id = UUID(user_id)

    except Exception as ex:
        return BaseOut(
            msg="Invalid uuid",
            error=str(ex)
        )

    for todo in db:

        if todo.id == user_id:

            todo.name = updatePost.name

            return TodoCreateOut(
                todo=todo,
                msg="name has been updated successfully"
            )

    return BaseOut(msg="no todo found::")

# endpoint to delete you todo as per the id

@delete_router.delete(
    '/todo/{user_id}',
    response_model=BaseOut
    )

def delete_todo(user_id:str) -> BaseOut:
    try:
        user_id = UUID(user_id)

    except Exception as ex:
        return BaseOut(
            msg="Invalid uuid",
            error=str(ex)
        )
    for i, todo  in enumerate(db):
        if todo.id==user_id:
            del db[i]
            return BaseOut(msg="todo deleted successfully")
    return BaseOut(msg="No such record with that particular id")



# getting the todo as per the category using a query parameter

@get_router.get(
    "/category",
    response_model=TodoGetOut | BaseOut
    )

def get_todos_as_per_catgory(category:str) -> TodoGetOut | BaseOut:
    todos:list[Todo]=[]
    for todo in db:
        if todo.category==category:
            todos.append(todo)

    if not todos:
        return BaseOut(msg=f"no any todo found with the category {category}")

    return TodoGetOut(todos=todos,msg="todo fetched successfuly")


routers=[get_router,post_router,delete_router,update_router]
for router in routers:
    app.include_router(router=router,prefix="/api")
    



