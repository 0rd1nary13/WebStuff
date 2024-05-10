from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

# Sample data for blog posts
fake_db = {}


class BlogPost(BaseModel):
    title: str
    content: str
    author: str


# HTML form for input
input_form = """
<form method="post">
    <label for="title">Title:</label><br>
    <input type="text" id="title" name="title"><br>
    <label for="content">Content:</label><br>
    <textarea id="content" name="content"></textarea><br>
    <label for="author">Author:</label><br>
    <input type="text" id="author" name="author"><br>
    <button type="submit">Submit</button>
</form>
"""


# Display the input form
@app.get("/", response_class=HTMLResponse)
async def display_form():
    return input_form


# Create a new blog post
@app.post("/", response_class=HTMLResponse)
async def create_post(request: Request):
    form_data = await request.form()
    post = BlogPost(title=form_data["title"], content=form_data["content"], author=form_data["author"])
    fake_db[post.title] = post
    return f"Post created: {post.title}"


# Retrieve all blog posts
@app.get("/posts/", response_class=HTMLResponse)
def read_posts():
    if not fake_db:
        return "No posts available."

    posts_html = "<h1>Blog Posts:</h1>"
    for post in fake_db.values():
        posts_html += f"<h2>{post.title}</h2>"
        posts_html += f"<p><strong>Author:</strong> {post.author}</p>"
        posts_html += f"<p>{post.content}</p>"
        posts_html += "<hr>"

    return posts_html


# Retrieve a specific blog post by title
@app.get("/posts/{title}", response_class=HTMLResponse)
def read_post(title: str):
    if title not in fake_db:
        raise HTTPException(status_code=404, detail="Post not found")

    post = fake_db[title]
    post_html = f"<h2>{post.title}</h2>"
    post_html += f"<p><strong>Author:</strong> {post.author}</p>"
    post_html += f"<p>{post.content}</p>"

    return post_html


# Delete a blog post by title
@app.delete("/posts/{title}", response_class=HTMLResponse)
def delete_post(title: str):
    if title not in fake_db:
        raise HTTPException(status_code=404, detail="Post not found")

    deleted_post = fake_db.pop(title)
    return f"Post deleted: {deleted_post.title}"
