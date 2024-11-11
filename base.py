from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Optional, List, Dict, Annotated
from pydantic import BaseModel, Field

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    age: int
class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User
class Postcreate(BaseModel):
    title: str
    body: str
    author: User
class UserCreate(BaseModel):
    name: Annotated[str, Field(..., title='Users Name', min_length=2, max_length=20)]
    age: Annotated[int, Field(..., title='age of user', ge=11, le=120)]

users = [
    {'id' : 1, 'name' : 'John', 'age' : 18},
    {'id' : 2, 'name' : 'Chan', 'age' : 30},
    {'id' : 3, 'name' : 'Felix', 'age' : 19}
]
posts = [
    {'id' : 1, 'title' : 'news1', 'body' : 'text1', 'author' : users[1]},
    {'id' : 2, 'title' : 'news2', 'body' : 'text2', 'author' : users[2]},
    {'id' : 3, 'title' : 'news3', 'body' : 'text3', 'author' : users[0]}
]
# @app.get('/items')
# async def items() -> List[Post]:
#     post_objects = []
#     for post in posts:
#         post_objects.append(Post(id=post['id'], title=post['title'], body=post['body']))
#     return post_objects

@app.get('/items')
async def items() -> List[Post]:
    return [Post(**post) for post in posts]

@app.post('/items/add')
async def add_items(post: Postcreate) -> Post:
    author = next((user for user in users if user['id']== post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail='user not found')

    new_post_id = len(posts) + 1

    new_post = {'id': new_post_id, 'title': post.title, 'body': post.body, 'author': author}
    posts.append(new_post)

    return  Post(**new_post)

@app.post('/user/add')
async def user_add(user: Annotated[
    UserCreate, Body(..., example={
        "name": "UserName",
        "age": 1
    })
]) -> User:
    new_user_id = len(users) + 1
    new_user = {'id': new_user_id, 'title': user.title, 'body': user.body, 'author'}
    users.append(new_user)
    return  User(**new_user)

@app.get('/items/{id}')
async def items(id: Annotated[int,Path(..., title='Здесь указывается id поста', ge=1, lt=100)]) -> Post:
    for post_search in posts:
        if post_search['id'] == id:
            return Post(**post_search)

    raise HTTPException(status_code=404,detail= 'post not found')

@app.get('/search')
async def search(post_id: Annotated[
    Optional[int],
    Query(title='ID of post to searh for', ge=1, le=50)
]) -> Dict[str,Optional[Post]]:
    if post_id:
        for post in posts:
            if post['id']== post_id:
                return {'data': Post(**post)}
        raise HTTPException(status_code=404, detail='post not found')
    else:
        return {'data' : None}

