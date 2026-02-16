---
code: TK06
title: API Design (Part 1)
date: 2026-02-16
due: 2026-02-19
type: task
threads: ["SDE / ADR", "Tools / Code Agent"]
authors: [Kris Jordan]
---

# TK06. API Design and Implementation

In this task you will design an API for a URL shortening service.

## Breakdown of Parts

Part 1. You only need to implement the route decorators and function signatures, *NOT* the actual implementations of the API.

Part 2. You will implement the API.

## App Overview: URL Shortener

In this lab, you and a partner will collaborate to design and implement a service that implements a URL-shortening API (submit a long URL and receive a short, redirectable URL).

This application will be able to generate shortened URLs, similar to UNC's `go.unc.edu` service which you can try out today. Here is an example of a shortened URL: <https://go.unc.edu/Xj9b6>

This application design will feature three personas:

1. **Sue Sharer** is someone who wants to distribute content easily. She might be a marketing manager sharing links to organization resources. Sue values convenience, control, and customization, which is why she wants options like vanity URLs and expiration times.

2. **Cai Clicker** is the person who receives and opens links. They might be a colleague reviewing content or a prospective customer. Cai values seamlessness and reliability—when they click a link, they expect to be redirected without delay.

3. **Amy Admin** is responsible for monitoring and managing all active links. She is a community manager. Amy values visibility, control, and order, ensuring that shared content remains appropriate and awareness of high-traffic links.

### User Journey Examples

An journey may combine a few user stories in order to give a complete start-to-finish example of a feature's use. Since you may not be familiar with the point of a URL shortener, consider these journeys before reading the user stories in a more standalone presentation.

### **Sue Sharer Creates a Shortened URL**  

1. Sue wants to a share a link to the company website <https://comp423-26s.github.io/>.  
2. She submits the long URL below and a vanity path of `comp423`:  
    ```
    https://comp423-26s.github.io/
    ```
3.  The system generates a link with the vanity path and responds with the information Sue needs to share the URL. 
4.  Sue shares this link with her friend: `https://<your-apps-hostname>/comp423` 
5.  Cai Clicker clicks the link and is redirected to:  
    ```
    https://comp423-26s.github.io/
    ```

### Required User Stories

1. As Sue Sharer, I want to create a shortened URL with an optional expiration time and the ability to request a custom vanity URL, so that I can control how long it is available and share a more meaningful link.
2. As Cai Clicker, I want to open a shortened URL by clicking its unique link, so that I am automatically redirected to the original long URL.
3. Amy Admin
    1. As Amy Admin, I want to see a list of all active resources (shortened URLs) and filter by type or view counts greater than some low threshold, so that I can oversee what content is currently being shared.  
    2. As Amy Admin, I want to see how many times each resource has been accessed, so that I can monitor usage and identify high-traffic resources.
    3. As Amy Admin, I want to change the target of a shortened URL, so that I can correct or modify existing resources when necessary.  
    4. As Amy Admin, I want to delete any active resource from the system, so that I can remove content that should no longer be available.  

### Path Requirement Specifications

User story 2 above is the only story which we will very specificaly share an API requirement, as follows:

The method is `GET` and the `path` in FastAPI route path syntax is `/{short_code}`.

* When a user accesses a vanity URL, the system must _**temporarily redirect**_ to a **shortened URL**.

### No Authentication Enforced

The concerns of how to authenticate a user, like Amy Admin, and authorize various actions, is beyond your concern in this initial API design. You should proceed with all routes publicly available, unprotected. Later, we'll learn strategies for authenticating and authorizing various actions at the HTTP API level.

## Phase 1: API Design

### Getting Started

To begin work on TK06, you and your partner will need to decide on _one of your TK05 implementations to serve as the starting point_. Begin by comparing approaches to _unit_ and _integration_ testing in TK05. If either of you did not reach 100% coverage for _unit_ and _integration_ testing, choose the partner's who did. If the approaches appear equivalent, flip a coin or play a game of rock-paper-scissors to decide whose will be the starting point. For instructional purposes, we will call the team mate whose TK05 repository will be the starting point the **starter**.

The way TK06's setup will work is that when the **starter** accepts the assignment through GitHub Classroom, they will set the team name of `team_tk06_NN` where `NN` is your team number from the [pairings sheet](https://docs.google.com/spreadsheets/d/1330dsHBdipQQbJWBTxrRvI05v9rUIFSRL9EnCewXaKE/edit?usp=sharing). The initial repository will be **empty**. In the starter's `tk05` repository, the empty `tk06` repository will be added as a **remote** and `main` will be pushed to it. From here, both team mates will clone the `tk06` repository to use for this next exercise.

**Starter** team mate's repository steps:

1. The **starter** (teammate whose TK05 repository will seed TK06's starting point) will accept the Github Classroom assignment here: <https://classroom.github.com/a/TZfqFme7>
    1. **Carefully* fill in your team name: `team_tk06_NN` where `NN` is your team's number from the [pairings sheet](https://docs.google.com/spreadsheets/d/1330dsHBdipQQbJWBTxrRvI05v9rUIFSRL9EnCewXaKE/edit?usp=sharing).
    2. You may need to view your GitHub invitations to accept the TK06 repository invitation in order to join the repository.
2. The **starter** will use their terminal (local) to navigate to TK05 and _add_ their new team repository as a remote repository:
    1. `git remote add tk06 [insert-tk06-repo-url-here]` - Replace the entire `[insert]` substring, square brackets included, with your empty TK06 repository URL.
    2. `git switch main` - If you are not already on the `main` branch.
    3. `git push tk06 main` - Push the `main` branch of your `tk05` to `tk06`.
3. Refresh the TK06 repository on GitHub to confirm it is no longer empty and contains your `tk05` repository's history as its starting point.

!!! success "Seeding New Repositories"

    As a team, reflect on what was just completed. It's very neat! You seeded a _new, empty_ repository by pushing a branch from an existing repository to it.

    This is commonly useful in real world scenarios and should make sense that it is possible with your understanding of what it means to `push` a branch to a remote. The neat feature of this particular scenario is the remote repository was empty and you were able to target it for your push by establishing a new remote named `tk06`.

**Both** team mate's next steps:

1. (Pre-step) The team mate who was _not the starter_ should go ahead and accept the GitHub classroom assignment and **carefully** select the correct team from the list of existing teams.
2. Using a terminal, both of you should navigate to the directory on your host machine's storage where you clone course projects.
3. **Both** team members should clone their `tk06` repository URL from GitHub using their host machine's terminal.
4. Open the TK06 repository in VSCode, then reopen the repository in a Dev Container.
5. Now you are ready to start!

!!! warning "Errors starting the Dev Containers in Windows"

    If you face a problem opening the DevContainer in Windows, it's likely due to a line ending issue. In VSCode, change your line ending setting for the project to be just LF _not_ CRLF. You will see a setting for this in the bottom right corner. Change to `LF` and try reopening the dev container.

### Create a Branch for Individual API Design

Clone the project, open your project in a dev container, and create a branch for your individual API design. **Name your branch something that includes your onyen or github username.**

### Individual API Design

In your branch created above, go ahead and stub out an HTTP API, making use of FastAPI routes and Pydantic models as necessary, that satisfy the user stories. Use the `/docs` user interface to review your routes. Your objectives are:

* **Define Endpoints**: Specify all the HTTP routes required for the required user stories above.
* **Design Data Models**: Create Pydantic models that define the structure of request bodies and responses.
* **Clear OpenAPI Documentation**: Fully document important your API using the OpenAPI standards discussed below.
* **Establish Conventions**: Ensure consistent naming and documentation throughout your API design.

### OpenAPI Specification Requirements

FastAPI and Pydantic have special constructs which allow you to more fully specify your API and its documentation to produce the standards-based `OpenAPI.json` spec powering the `/docs` user interface.

You are **required** to add specification and documentation to your API design along each of the following dimensions. You can find examples of how each is done following this overview list:

- **FastAPI Application:** Ensure your app is properly instantiated with required metadata.
- **Route-level:** Always include a summary and description; document response bodies thoroughly.
- **Route Parameters:**
    - **Path parameters:** Must have descriptions and optional validations.
    - **Query parameters:** Must have descriptions and can include validations.
    - **Body parameters:** Must have descriptions and `openapi_examples` for clear request body documentation.
- **Pydantic Fields:** Every field should include a description and an example (or examples) to aid API consumers.

#### FastAPI Application-level Documentation

Instantiate your FastAPI app using the `FastAPI` constructor. You *must* provide a `title`, `contact`, `description`, and `openapi_tags` (for organizing routes), as shown below. Notice that the description is markdown and you can use a _docstring_ to give your API documentation 

*Example:*

```python
app = FastAPI(
    title="TK06 API Design",
    contact={
        "name": "Parter A, Partner B",
        "url": "https://github.com/comp423-26s/<your-team-repo>",
    },
    description="""
## Introduction

Your introduction text to your API goes here, in **markdown**.
Write your own brief intro to what his API is about.
""",
    openapi_tags=[
        {"name": "Sue", "description": "Sue Sharer's API Endpoints"},
        {"name": "Cai", "description": "Cai Clicker's API Endpoints"},
        {"name": "Amy", "description": "Amy Admin's API Endpoints"},
    ],
)
```

After you've more fully configured your `app`, as shown above, try reloading your OpenAPI UI by navigating to `/docs` in your dev server. You should see the information above being used to improve the documentation generated. The **tags** added will allow you to organize your routes based on the intended user. In real APIs, tags are generally used to cluster endpoints for a specific feature together; here we're using them to organize by persona served.

#### Route-level Decorator Specification

Define endpoints using FastAPI’s route decorators (e.g., `@app.get`, `@app.post`). Each route *must* include a *summary*, *description*, and *tag*. The *tag* corresponds to the `openapi_tags` you specified above and will be a persona name. If your route returns response codes besides `200`, such as `404`, you need to specify the *responses* field as shown below. For a given status code, the *description* is required and the *model* (Pydantic subclass) is only necessary if the response returns a body.

*Example:*

```python
from typing import Annotated

class MessageResponse(BaseModel):
    message: Annotated[str, Field(
        description="Information conveyed ot user", examples=["Hi!"]
    )]

# ...

@app.get(
    "/items/{item_id}",
    summary="Retrieve an Item",
    description="Get details of an item by its ID.",
    responses={
        404: {
            "description": "Item not found",
        }
    },
    tags=["Shopping"]
)
def get_item(item_id: int) -> MessageResponse:
    if item_id > 0:
        return MessageResponse(message="Item found!")
    else:
        raise HTTPException(status_code=404, detail="Item not found!")
```

#### Dynamic **Path** Parameters

For dynamic segments in the URL (path parameters), use `Path`. Include a **description** and any additional keyword parameters found in the [official documentation](https://fastapi.tiangolo.com/reference/parameters/?h=path%28#fastapi.Query) you believe would be helpful in specifying and documenting your path (useful ideas: 1. `examples` list of example values you might expect for the parameter, 2. validation such as `min_length` or `gt` (greater than) as shown below).

*Example:*

```python
from fastapi import FastAPI, Path
from typing import Annotated

# ...

@app.get("/users/{user_id}")
def get_user(
    user_id: Annotated[int, Path(
        description="The unique ID of the user",
        gt=0,
        examples=[1, 423]
    )]
) -> User:
    ...
```

#### **Query** Parameters

For query parameters (appended to the URL), use `Query`. Each query parameter **must** include a **description**, **should** probably include a default value, and can optionally include additional examples and validation rules, if needed. See the [official documentation](https://fastapi.tiangolo.com/reference/parameters/?h=path%28#fastapi.Query) on supported keyword parameters when specifying and documenting query parameters.

*Example:*

```python
from fastapi import FastAPI, Query
from typing import Annotated

# ...

@app.get("/search")
def search_items(
    q: Annotated[str, Query(
        description="The product search query",
        examples=["jordans"]
    )] = "" # Default value is empty string
) -> SearchResults:
    ...
```

#### Documenting Pydantic Model Fields

Within your Pydantic models, use the `Field` function to document each field. Every field **must** have a **description** and **examples** list to aid API consumers.

*Example:*

```python
from pydantic import BaseModel, Field
from typing import Annotated

class Item(BaseModel):
    name: Annotated[str, Field(
        description="Name of Product",
        examples=["UNC Jersey", "UNC Socks"]
    )]
    price: Annotated[float, Field(
        description="Sales Price",
        examples=[75.0, 20.0]
    )]
```

#### Request Body Parameters

For request body parameters (used in `POST`/`PUT`/`PATCH` requests), define a Pydantic model and use `Body` to add metadata. The body parameter **must** include a **description** and **openapi\_examples**. These examples help make testing out the API in `/docs` easier, as you will see when you try it out. You can also add validation rules if needed.

*Example:*

```python
from fastapi import FastAPI, Body
from typing import Annotated

# ... Same Item model as above ...

@app.post("/items")
def create_item(
    item: Annotated[Item, Body(
        description="The product to create",
        openapi_examples={
            "Air Jordans": {
                "summary": "Air Jordan 1 Mid SE",
                "description": "Sample product to create",
                "value": {
                    "name": "Air Jordan 1 Mid SE",
                    "price": 134.99
                },
            }
        }
    )]
) -> Item:
    ...
```

### Collaboration for Phase 1

Each of you should individually draft a design of your API in FastAPI on your own branches (branch naming specified after the Getting Started section above). You should both push your branches to GitHub.

Once you are ready to merge your branches to form a unified API for your team, we do not recommend actually attempting a merge in `git`. You are welcomed to, but at your own peril. Since you both worked in `main.py`, and made design decisions independently, the merge conflict resolution will be gnarly.

Instead of attempting a `git` merge, we strongly suggest **pair programming**, and starting over by going back to your `main` branch on one of your machines. Start a new branch based on `main` that is `pair-api-design`. On the other of your machines, have open both of your branches in GitHub to easily view how each of you approached the design and try to form a consensus on how to approach. You will be well served by each reading each other's design and then attempting to whiteboard your final approach before diving into code. Once you are complete, push your final `pair-api-design` to GitHub and submit your teams' reflection for Phase 1 on Gradescope.

### Sanity Checks

Questions to consider in the context of your API:

* Have we ensured that our design addresses every required user story for Sue, Cai, and Amy?
* Are our naming conventions for endpoints, models, and fields consistent and descriptive enough for all personas?
* Are we including required metadata (e.g., summaries, descriptions, examples) for every endpoint and model field so that a developer can easily understand our API?
* How have we documented error responses (like 404 for missing resources) in our endpoints?
* Is the route design intuitive for both API users and maintainers?

### Phase 1 Submission and Reflection Questions

* Gradescope submission will include:
    * Permalink to branches of both partners
    * Permalink to the final `pair-api-design` branch
* Brief reflection question:
    * What challenges did we encounter when comparing our individual designs, developing a single design, and pair programming our joint, final design?

### Key Takeaways

1. **Designing for Users and Use Cases**

    Through this assignment, you’ve gained experience designing an API that serves multiple types of users with distinct needs. You’ve seen how clear, user-focused API design is essential—not just for making the system functional but also for ensuring a smooth experience for different personas. This mirrors real-world software development, where balancing the needs of end users, system administrators, and stakeholders is key to building successful products.

2. **Writing Clear, Professional API Documentation**

    By leveraging FastAPI’s OpenAPI documentation, you’ve practiced writing API specs that go beyond just making things work, you’ve created an API that is easy for others to understand, test, and use. In industry, well-documented APIs are what enable teams to scale, integrate with other systems, and onboard new developers quickly. This attention to detail will serve you well in any software engineering or product development role.

3. **Collaborating on Software Design in a Team Environment**

    By independently designing an API and then merging your ideas into a unified implementation, you’ve practiced an essential part of professional software development: balancing individual contributions with collaborative decision-making. You’ve navigated trade-offs, discussed design choices, and worked toward a shared vision. These skills are essential in any software engineering role.

4. **Designing the Interface First for Human-Centered Development**

    By focusing on the API interface before implementation, you’ve embraced a human-centered approach: prioritizing how users interact with the system rather than getting lost in internal details. This ensures the design is intuitive and valuable. A well-defined interface also enables parallel development: frontend teams can build against the spec while backend teams implement functionality, making collaboration more efficient. In real-world projects, this approach reduces wasted effort, improves usability, and accelerates development, ultimately leading to better software.

