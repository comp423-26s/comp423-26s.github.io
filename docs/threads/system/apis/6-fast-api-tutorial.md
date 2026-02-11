---
code: RD16
title: "FastAPI and Pydantic Tutorial"
date: 2026-02-11
due: 2026-02-15
type:  reading
threads: ["System / APIs"]
authors: [Kris Jordan]
---

# 6. FastAPI and Pydantic Tutorial

FastAPI is a modern, fast (high-performance), standards-first web framework for Python.
It's designed around modern Python features such as type annotations (like you used in COMP110). FastAPI helps you both _specify_ and build RESTful HTTP APIs quickly.

Pydantic is a library used by FastAPI for data modeling and validation. It is how we will specify the schemas for request and response body data. It enforces type hints at runtime and yields user-friendly errors.

Since you are now comfortable with HTTP methods, paths, query parameters, and so on, from the previous parts of this reading, you're in great shape to dive in!

## 1. Getting Started

In a terminal on your host machine, outside of any other `git` repositories, follow the following steps:

1. **Clone the tutorial repository**: Start by cloning the repository at [https://github.com/comp423-26s/fastapi-tutorial.git](https://github.com/comp423-26s/fastapi-tutorial.git).

2. **Open the repository in a VS Code Dev Container**. The dev container is based on a modern Microsoft Dev Container image, which we have already used once in this course, so it should load quickly and install the necessary dependencies from `requirements.txt`. This repo uses an older style package manager (`pip`) than what we have emphasized this semester (`uv`), but both tools and setups are valid and common "in the wild."

3. **Open main.py**. This is the entrypoint of our API app and where the tutorial starts!

## 2. First Route: Hello World

There's only one way to venture into new territory in programming: _hello, world!_ Let’s start with the simplest possible route. Update your `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root() -> str:
    return "Hello, world!"
```

### What Does `@app.get("/")` Mean?

- **Decorator**: If you’re new to decorators, think of `@something` as a way to wrap or register the function that follows. In this case:
    - `@app.get("/")` tells FastAPI that this function (`read_root`) handles **GET** requests to the **root path** (`"/"`).
    - The function name `read_root` is arbitrary—choose a meaningful name for your own clarity.
- When you return a string (like `"Hello, world!"`), FastAPI automatically converts it into an HTTP response with the body containing that string.

---

## 3. Running the Development Server

To run your app in development, use the following command (from within the `fastapi-tutorial` folder):

```bash
fastapi run main.py --reload
```

By default, FastAPI’s dev server:

- Runs at `http://127.0.0.1:8000` (port 8000). **Note: If you have any other dev servers running on this same port (e.g. your MkDocs project's dev server) see the Ports tab in VSCode to learn what port this container's 8000 was mapped to on your host machine.**
- The `--reload` argument causes the server to watch your files. If you make changes, it **auto-reloads** so you don’t have to stop and restart the server on every change you make to your code.

Behind the scenes, **FastAPI** is using a Python package called **Uvicorn** to handle lower-level HTTP concerns. This is beyond your concern, but if you see anything about `uvicorn` when reading about FastAPI just know it's a foundational HTTP layer that FastAPI sits above in the architecture. 

Whenever a request hits `GET /`, it calls our `read_root()` function.

Take a look at your Python code and be sure you can identify where the following HTTP API dimensions are specified: the **HTTP method** (1), the **path** (2), and the **response body schema** (3). Click the annotation icon, the plus symbol, to expand the answers.
{ .annotate }

1. The HTTP method is specified in the `@app.get` annotation (`GET`). If it makes it easier to remember, HTTP method specification in FastAPI is implemented as a _method call_ on the FastAPI `app` object.

2. The _path_ is `/`, commonly called a root path since it has no parts beyond the slash, and it is specifed as the first parameter of the `@app.get()` method call.

3. The _response body schema_ is specified as the _return type_ of the route handler function. In this case it is `str` as the returned value is `"Hello, world!"`.

---

## 4. Adding Another Static Route

Let’s add a second route, say, `GET /about` which returns some simple text. Update your `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root() -> str:
    return "Hello, world!"

@app.get("/about")
def read_about() -> str:
    return "This is a simple HTTP API."
```

Try visiting `http://localhost:8000/about`. You should see the alternate message!

---

## 5. Introducing a Pydantic Model and Listing Posts

Next, let’s introduce a **Pydantic** model to represent our data. These models serve a dual purpose: first they give us a Python class we can use throughout our server-side code. Second, in conjunction with FastAPI, they will automatically create a schema for our API specifications.

We’ll use a simple "Post" resource as an example throughout this tutorial. Let's start by returning a list of posts from a global dictionary that we’ll pre-populate with a couple sample posts.

1. Define the `Post` model as a subclass of `pydantic.BaseModel`. Be sure to add the `import` statement for `BaseModel`. Define it to have two attributes: `id` and `content`.
2. Create a global dictionary `posts_db` containing two posts keyed by their IDs.
3. Add a route `GET /posts` to **list** all posts.

Update `main.py` with the following:

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

class Post(BaseModel):
    id: Annotated[int, Field()]
    content: Annotated[str, Field()]

# Prepopulate dictionary of posts
posts_db = {
    1: Post(id=1, content="Hello FastAPI!"),
    2: Post(id=2, content="Writing my second post!")
}

@app.get("/")
def read_root() -> str:
    return "Hello, world!"

@app.get("/about")
def read_about() -> str:
    return "This is a simple HTTP API."

@app.get("/posts")
def list_posts() -> list[Post]:
    return list(posts_db.values())
```

### How This Works
- We store two example posts in a global dictionary, `posts_db`, keyed by their ID.
- The route `GET /posts` returns `list(posts_db.values())`, which effectively returns **all** posts as a list.
- Notice how each value in `posts_db` is already an instance of `Post`. When FastAPI sees these objects, it converts them to JSON automatically.

Notice the return type of the `list_posts` function is a `list` of `Post` objects. This is specifying the response body schema. Try visiting this route in your browser to confirm it is working. If you do not see well formatted JSON that is easy to read, try going back to the previous part of this reading and installing a JSON Viewer plugin in your web browser.

---

## 6. Adding a Dynamic Route to Get a Single Post

Now let’s introduce our first **dynamic** route. For a URL like `"/posts/1"`, we want to look up the post with `id=1` in our dictionary and return the `Post` object with this ID. 

Add the following import and route definition to your `main.py` file:

```python
# ... Update FastAPI Imports ...
from fastapi import FastAPI, HTTPException, Path
from typing import Annotated

# ... Earlier App Stays Same ... 

@app.get("/posts/{post_id}")
def get_post(post_id: Annotated[int, Path(title="ID of Post")]) -> Post:
    if post_id in posts_db:
        return posts_db[post_id]
    raise HTTPException(status_code=404, detail="Post not found")
```

### Try a Happy Path

Try navigating to `/posts/1` and `/posts/2` and convince yourself you can trace the flow of information. Specifically, look at how the _path_ is specified with a dynamic part named `post_id` and how that path part corresponds to the function parameter of the same name. The value is then used to lookup a post with a given ID in the dictionary.

### Try an Unhappy Path

Try navigating to `/posts/3` and seeing the 404 Response. Your browser won't show you the response code directly, but you can open up your browser's Developer Tools and look at your Network history (try reloading) to see the 404 is being sent. Notice this is achieved programatically in FastAPI by raising an `HTTPException` with a `status_code` keyword parameter.

### Try an Invalid Path

Finally, navigate to `/posts/abc`. Because we declared `post_id: int`, FastAPI automatically checks if `"abc"` can be converted to an integer. It cannot, so the framework responds with an HTTP **422 Unprocessable Entity** error, including a helpful error message about the invalid type. This automatic validation is one of the many reasons FastAPI is a joy to work with compared to its predecessors! Edge case handling like this used to require more boilerplate code from engineers.

---

## 7. Understanding Routing in Modern API Frameworks

Now that you’ve seen both a static route (`"/posts"`) and a dynamic route (`"/posts/{post_id}"`), let’s briefly discuss how routing works in a modern framework like FastAPI. At a high-level, the routing algorithm works like this:

1. **Match the HTTP method** (GET, POST, PUT, DELETE, etc.).
2. **Match the path pattern** (`"/"`, `"/about"`, `"/posts"`, `"/posts/{post_id}"`, etc.).
    * Routes are checked _in the order they are defined_ which can be surprising. If you define a route like `/posts/{post_id}` and then a route like `/posts/stats` follows it, the first route will always be matched (and error). To avoid this common issue, specify routes with static path parts before the dynamic path parts.
3. **Handle parameters** (like `post_id`) including type conversion and validation.
4. **Call the function** associated with that route.
5. **Return a response** which might be JSON, HTML, or something else.

Like everything, there is a bit more more machinery behind the scenes, but understanding routing at this level of details is sufficient for now.

---

## 8. Automatic Documentation with OpenAPI

One major benefit of FastAPI is its automatic generation of **OpenAPI** documentation. OpenAPI was previously known as Swagger, which was an objectively awful name, so this is a welcomed development in the community. By default, FastAPI sets up:

- An **OpenAPI specification** at `/openapi.json`.
- An OpenAPI-based **web interface** at `/docs`.

With your FastAPI dev server is running, navivate to:

- **`/docs`** — a graphical user interface where you can see all endpoints, query them, and see sample requests and responses.
- **`/openapi.json`** — the raw JSON specification for your API.

Because we used `pydantic.BaseModel` for `Post`, the schema's model shape will be visible in `/docs`, including field types and potential validation error states.

!!! note "Why is an OpenAPI spec valuable?"

    - It standardizes your API contract, so other developers or tools (like code generators) know exactly how to consume your endpoints.
    - The `/docs` interface provides a quick way to try out your endpoints. This will be valuable in the next section.

### OpenAPI UI in the Wild: CSXL.unc.edu

To hopefully drive home the point that what you are learning is both _real_ and used in the wild, try opening up this URL in a new tab: <https://csxl.unc.edu/docs>.

This is the API for the CSXL web application. Many routes require an authentication token. If you want to try those routes, in a separate tab open up the CSXL website, login, and go to your user profile. Under profile actions, click "Copy" on the Bearer Token (which is an authorization key for your user). Paste that in to the `/docs` unlock screen. Then try running the `GET /api/profile` API endpoint and you should see your data.

Some other fun routes include public ones like listing student organizations or classes in a given semester.

If you've used office hours via the CSXL, or applied to be a TA, or reserved a room or checked into the XL Coworking space for a desk to work at... _you've already used this API without knowing it_! If you scroll around you can see the API end points powering coworking, office hours, and more.

---

## 9. Adding a POST Route

Let’s make our API a bit more dynamic by allowing clients to **create** new posts. We’ll maintain our dictionary `posts_db` but now add a route for **POST**. We can do something like this:

```python
# Update FastAPI Imports
from fastapi import FastAPI, HTTPException, status, Body

# ... Keep other routes the same ...

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Annotated[Post, Body()]):
    if post.id in posts_db:
        raise HTTPException(status_code=400, detail="Post with this ID already exists")
    posts_db[post.id] = post
    return post
```

### Walkthrough of the POST Route
- **Request Body**: FastAPI automatically parses the incoming JSON body into a `Post` object (thanks to Pydantic). Notice how simple this is! We specified a parameter to the function of a Pydantic model type, there is no conflicting name in a dynamic path part, so FastAPI _convention_ infers this must be the schema of the data in the request body.
- We "**store**" that post in `posts_db` using the post’s `id` as the key.
- By specifying `status_code=status.HTTP_201_CREATED`, FastAPI will return a **201 Created** status code upon success.
- We also added a small check to ensure that an existing post with the same ID doesn’t get overwritten.

Open your browser to the API UI page `/docs`, or reload it (this page will not automatically refresh upon saving your work in the editor). Scroll to the `POST /posts` endpoint. You can:

1. Click **Try it out**.
2. Provide a sample JSON body, e.g.:
   ```json
   {
     "id": 3,
     "content": "My brand new post!"
   }
   ```
3. Click **Execute** and see the response information.

You can then go to the `GET /posts/{post_id}` endpoint in `/docs` (or directly at `/posts/3`) to verify the newly created post.

There are a few other activities for you to try here:

1. Try posting the same JSON and seeing the response code.
2. Try posting a JSON body that is just `{"id": 4}` and seeing the response FastAPI produces. (WOW!)
3. Look at the specific response status code of the happy path (201) in the `/docs` UI. Notice where this is coming from in the definition. Take a look at how this is specified in the decorator as an additional parameter. There are other ways of responding with a specific status code, but this is preferred in a case like this.

!!! warning "Your 'Database' of Posts Will Reset"

    We are not actually using a "database" in this tutorial; just a dictionary stored in our module's global memory a sa simplification. As such, every time your FastAPI server stops and restarts, this dictionary is reset to its initialized contents. That means each time you change your `main.py` file below, and the server automatically reloads, you will lose any changes made via the API.

    Soon, we will learn how to connect our API to persistent databases that live in a layer outside of our code such that when we stop and restart our server the data is securely stored and accessible again as soon as our server starts back up.

---

## 10. Adding PUT and DELETE

Finally, let’s round out our basic CRUD functionality (Create, Retrieve, Update, Delete) with **PUT** (update) and **DELETE** HTTP method routes. Here’s a simple approach, using our dictionary to check for existence by key:

```python
# ... previous code remains the same ...

@app.put("/posts/{post_id}")
def update_post(post_id: Annotated[int, Path()], updated_post: Annotated[Post, Body()]) -> Post:
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    posts_db[post_id] = updated_post
    return updated_post

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: Annotated[int, Path()]) -> None:
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts_db[post_id]
    return None # 204 = No Content
```

### PUT: Update a Resource
At the HTTP specification level, **PUT** is meant to **replace** the resource at the specified URL. Here, our resource is `"/posts/{post_id}"`. When the client requests `PUT /posts/5`, for example, we expect the request body to provide the new `id` and `content` fields for post `5` (or whichever post ID is specified). If that post doesn’t exist, we respond with a **404 Not Found**.

### DELETE: Remove a Resource
Similarly, **DELETE** aligns directly with the idea of removing the resource at the URL. When a client requests `DELETE /posts/5`, we remove post `5` from our `posts_db`. A successful removal returns a **204 No Content**, which communicates that the request succeeded, but there’s no response body.

### Testing PUT and DELETE in the OpenAPI UI

1. **Open the documentation**: Navigate to `http://localhost:8000/docs`. You’ll see your new `PUT` and `DELETE` endpoints under the `/posts/{post_id}` section.
2. **Try PUT**:
    - Expand **PUT /posts/{post_id}**.
    - Click **Try it out**.
    - Enter a valid `post_id` (e.g., `1`) in the path parameter box.
    - Provide a JSON body with the `id` and `content` fields. For instance:
        ```json
        {
        "id": 1,
        "content": "Updated content via PUT!"
        }
        ```
    - Execute the request and verify that the response shows the updated post.
    - Try using the `GET` routes (list or by ID) to confirm the update is reflected following the update.
3. **Try DELETE**:
    - Expand **DELETE /posts/{post_id}**.
    - Click **Try it out**.
    - Enter the `post_id` for the post you want to remove.
    - Execute, and you’ll see a **204** response indicating success (no body returned).
    - If you try a `post_id` that doesn’t exist, you’ll get a **404 Not Found**.
    - Try using the `GET` routes (list or by ID) to confirm the `POST` as deleted from your in-memory "database".

With **PUT** and **DELETE**, you now have the full set of HTTP operations to manage a simple resource.

---

## Summary and Next Steps

Congratulations! You’ve:

1. Declared routes with static paths (`"/"`, `"/about"`).
2. Introduced **Pydantic** models (`Post`) and used a global dictionary to store and retrieve posts.
3. Created routes to list all posts, get a specific post by ID (dynamic route), and handled invalid IDs.
4. Learned how FastAPI automatically validates path parameters.
5. Explored how FastAPI auto-generates **OpenAPI** docs at `"/docs"`.
6. Implemented **POST**, **PUT**, and **DELETE** to complete the CRUD operations set.

### Best Practices Beyond This Tutorial

- **Organize your files**: Real projects separate routers, models, and database logic into different modules.
- **Use databases**: Instead of an in-memory dictionary, integrate a real database system for persistence.
- **Validation and error handling**: Explore more Pydantic features to ensure robust data validation. One place where we did not fully specify our APIs above, for the sake of not getting bogged down in error cases, is when we responded with error status codes but did not specify this in the route decorator. In the next assignment, we will fully specify all expected response types in our route handler functions.

With these fundamentals, you have a solid handle on building a basic API with **FastAPI**. Enjoy experimenting, and happy coding!
