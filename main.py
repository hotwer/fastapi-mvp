from Models.Blog import Blog
from Services.BlogService import BlogService 
from fastapi import FastAPI

app = FastAPI()
blog_service = BlogService()

@app.get('/')
def home():
    return ["Hello", "World"]

@app.get('/blogs', response_model=list[Blog])
def get_blogs():
    return blog_service.all()

@app.put('/blogs', response_model=Blog)
def insert_blog(item: Blog):
    return blog_service.insert(item)

@app.patch('/blogs', response_model=Blog)
def update_blog(item: Blog):
    return blog_service.update(item)

@app.get('/blogs/{id}', response_model=Blog)
def get_blog(id: str):
    return blog_service.get(id)

@app.delete('/blogs/{id}')
def delete_blog(id: str):
    res = blog_service.delete(id)
    return { 'message': 'Blog deleted succesfuly' if res.deleted_count > 0 else 'Blog not found for deletion' }


