# EX01. API Design and Implementation

## Breakdown of Parts

Part 1. You only need to implement the route decorators and function signatures, *NOT* the actual implementation of the API.

Part 2. You wll implement the API and deploy it to a production environment.

## App Overview: The Pastebin + URL Shortener

In this lab, you and a partner will collaborate to design and implement a service that combines:

* A Pastebin-style API (store text snippets and retrieve them by a unique URL).
* A URL-shortening API (submit a long URL and receive a short, redirectable URL).

These two functionalities must share a common **opaque namespace** for links, presenting unique design challenges regarding how to store and retrieve resources come implementation time.

This application will be able to generate shortened URLs for sharing content such as:

1. Pastbin Example: <https://pastebin.com/uYCCWaxy>
2. URL Shortener Example: <https://go.unc.edu/Xj9b6>

This application design will feature three personas:

1. **Sue Sharer** is someone who wants to distribute content easily. She might be a student sharing notes, a blogger sharing a quote, or a prankster hiding a Rickroll. Sue values convenience, control, and customization, which is why she wants options like vanity URLs and expiration times.

2. **Cai Clicker** is the person who receives and opens links. They might be a friend reading a shared snippet, a recruiter reviewing a resume, or an unsuspecting victim of a disguised meme. Cai values seamlessness and reliability—when they click a link, they expect to either see content immediately or be redirected without confusion.

3. **Amy Admin** is responsible for monitoring and managing all active resources. She is a community manager. Amy values visibility, control, and order, ensuring that shared content remains appropriate and awareness of high-traffic links.

### User Journey Examples

An journey may combine a few user stories in order to give a complete start-to-finish example of a feature's use. Since you may not be familiar with the point of a pastebin-like service, or URL shortener, consider these journeys before reading the user stories in a more standalone presentation.

### **Sue Sharer Creates a Text Snippet**  

1. Sue wants to share a quote from a book with a friend.  
2.  She submits the text:  
    ```
    "Not all those who wander are lost."
    ```
3.  The system generates a random URL path and responds with the information Sue needs to share the URL.
4.  Sue shares this link with her friend.  
5.  Cai Clicker clicks the link, which looks something like `https://<your-apps-hostname>/xYzA12` and sees the text snippet:  
    ```
    "Not all those who wander are lost."
    ```

### **Sue Sharer Creates a Shortened URL**  

1. Sue wants to prank a friend by disguising a Rick Astley video link.  
2. She submits the long URL below and a vanity path of `exam-solutions`:  
    ```
    https://www.youtube.com/watch?v=dQw4w9WgXcQ
    ```
3.  The system generates a link with the vanity path and responds with the information Sue needs to share the URL. 
4.  Sue shares this link with her friend: `https://<your-apps-hostname>/exam-solutions`  
5.  Cai Clicker clicks the link and is redirected to:  
    ```
    https://www.youtube.com/watch?v=dQw4w9WgXcQ
    ```

### Required User Stories

1. Sue Sharer
    1. As Sue Sharer, I want to create a new text snippet with an optional expiration time and the ability to request a custom vanity URL, so that I can control how long it is available and share a more meaningful link.
    3. As Sue Sharer, I want to create a shortened URL with an optional expiration time and the ability to request a custom vanity URL, so that I can control how long it is available and share a more meaningful link.
2. Cai Clicker
    1. As Cai Clicker, I want to open a shared text snippet by clicking its unique link, so that I can read the content that was provided to me.
    2. As Cai Clicker, I want to open a shortened URL by clicking its unique link, so that I am automatically redirected to the original long URL.
2. Amy Admin
    1. As Amy Admin, I want to see a list of all active resources (text snippets and shortened URLs) and filter by type or view counts greater than some low threshold, so that I can oversee what content is currently being shared.  
    2. As Amy Admin, I want to see how many times each resource has been accessed, so that I can monitor usage and identify high-traffic resources.
    3. As Amy Admin, I want to update the content of an active text snippet or change the target of a shortened URL, so that I can correct or modify existing resources when necessary.  
    4. As Amy Admin, I want to delete any active resource from the system, so that I can remove content that should no longer be available.  

### Path Requirement Specifications

User stories 2.a. and 2.b. above are the only stories which we will very specificaly share an API requirement, as follows:

These two stories should both share the same opaque route, including *method* and *path*. The method is `GET` and the `path` in FastAPI route path syntax is `/{resource_identifier}`. This means that there is a single shared path pattern for retrieving both types of resources.

* When a user accesses a generated or vanity URL, the system must determine whether it corresponds to a **text snippet** or a **shortened URL**.
* The user **should not** be able to infer whether a given URL points to a text snippet or a redirection just by looking at it.

### No Authentication Enforced

The concerns of how to authenticate a user, like Amy Admin, and authorize various actions, is beyond your concern in this initial API design. You should proceed with all routes publicly available, unprotected. Later, we'll learn strategies for authenticating and authorizing various actions at the HTTP API level.

## Phase 1: API Design

### Getting Started

To begin work on EX01, you and your partner will need to accept a GitHub classroom with your ==assigned Team Name (in the form of **`team_0_NN`**)== found in the [pairings sheet](https://docs.google.com/spreadsheets/d/1Eu4tzOATIkRDSwg9NqxZleKChDjYhuQD8ORjOspsNMg/edit?usp=sharing). First look up your team name by your PID and copy it. Then go accept the [GitHub classroom assignment by following this link](https://classroom.github.com/a/FfbRXDWO). Search for your team name and if it already exists, join it. If you are the first of your pair to begin, create the team with the assigned team name.

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

You are required to add specification and documentation to your API design along each of the following dimensions. You can find examples of how each is done following this overview list:

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
    title="EX01 API Design",
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

### A Note on Model Design and Typing

In your design space for implementing your models, there are likely a few paths worth considering. The design challenge you are confronted with is your API involves two different kinds of resources (text versus links) and they have differences in behaviors, validations, and so on. However, they also share some things in common (such as the namespace for their shortened paths once created, the expiration, and the access counter).

1. (Do not do this!) Unimodel - Single model shared by both types. This solution is taking on technical debt and becomes gnarly to maintain and extend.
2. (Discouraged) Traditional Inheritance Hierarchy - a single resource subclass of `BaseModel` which is then subclassed for your specific resources.
3. (Recommended) [Discriminated Type Unions](https://docs.pydantic.dev/2.0/usage/types/unions/#discriminated-unions-aka-tagged-unions) - models use a common string field to communicate their type. This is useful because once a Python or JavaScript object is _serialized_ into JSON for transfer over an API, only the field names and values of an object are transferred. By encoding type into a field, it's easier to work with. This strategy has emerged in many dynamic programming languages and is recommended in Pydantic and our front-end language TypeScript.

To learn more about discriminated type unions in Pydantic, see the [official Pydantic documentation]. Additionally, feel free to search or have an [interactive learning conversation with ChatGPT](https://chatgpt.com/share/679f8a1a-22d4-8000-8ad4-2dab48c5f46f) to gain a better understanding. [Here's an example prompt I tried in ChatGPT that gave a solid introduction](https://chatgpt.com/share/679f8a1a-22d4-8000-8ad4-2dab48c5f46f). As always, with LLM generated content, read carefully and vigilantly: it doesn't always tell the complete story, the correct story, or have a complete understanding of what exactly you are doing.

### Collaboration for Phase 1

Each of you should individually draft a design of your API in FastAPI on your own branches (branch naming specified after the Getting Started section above). You should both push your branches to GitHub.

Once you are ready to merge your branches to form a unified API for your team, we do not recommend actually attempting a merge in `git`. You are welcomed to, but at your own peril. Since you both worked in `main.py`, and made design decisions independently, the merge conflict resolution will be gnarly.

Instead of attempting a `git` merge, we strongly suggest **pair programming**, and starting over by going back to your `main` branch on one of your machines. Start a new branch based on `main` that is `pair-api-design`. On the other of your machines, have open both of your branches in GitHub to easily view how each of you approached the design and try to form a consensus on how to approach. You will be well served by each reading each other's design and then attempting to whiteboard your final approach before diving into code. Once you are complete, push your final `pair-api-design` to GitHub and submit your teams' reflection for Phase 1 on Gradescope.

### Sanity Checks

Questions to consider in the context of your API:

* Have we ensured that our design addresses every required user story for Sue, Cai, and Amy?
* Are our naming conventions for endpoints, models, and fields consistent and descriptive enough for all personas?
* How does our design distinguish between a text snippet and a URL shortener resource when using the same `/{resource_identifier}` endpoint?
* Are we including required metadata (e.g., summaries, descriptions, examples) for every endpoint and model field so that a developer can easily understand our API?
* How have we documented error responses (like 404 for missing resources) in our endpoints?
* Is the route design intuitive for both API users and maintainers?
* How easily can our design be extended in the future if new requirements are added?

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

    By leveraging FastAPI’s OpenAPI documentation, you’ve practiced writing API specs that go beyond just making things work—you’ve created an API that is easy for others to understand, test, and use. In industry, well-documented APIs are what enable teams to scale, integrate with other systems, and onboard new developers quickly. This attention to detail will serve you well in any software engineering or product development role.

3. **Navigating Design Constraints**

    You’ve tackled a unique design challenge: storing and retrieving two different resource types (text snippets and URL redirects) while keeping a shared, opaque namespace. This required careful thinking about data modeling and routing logic. Real-world software design often involves trade-offs like these, where multiple features must coexist within a unified system without exposing unnecessary complexity to users.

4. **Collaborating on Software Design in a Team Environment**

    By independently designing an API and then merging your ideas into a unified implementation, you’ve practiced an essential part of professional software development: balancing individual contributions with collaborative decision-making. You’ve navigated trade-offs, discussed design choices, and worked toward a shared vision—skills that are essential in any software engineering role.

5. **Designing the Interface First for Human-Centered Development**

    By focusing on the API interface before implementation, you’ve embraced a human-centered approach—prioritizing how users interact with the system rather than getting lost in internal details. This ensures the design is intuitive, valuable, and easy to integrate. A well-defined interface also enables parallel development: frontend teams can build against the spec while backend teams implement functionality, making collaboration more efficient. In real-world projects, this approach reduces wasted effort, improves usability, and accelerates development, ultimately leading to better software.


## Phase 2: Implementation

In this phase of the exercise, you will implement a service layer in order to have a functional API. All of your Phase 2 business logic should be in the service layer. Your routes should only address HTTP concerns and otherwise delegate control to your service(s).

Before beginning on Phase 2, you should complete the following readings and submit them on Gradescope:

* [Layered Architecture](../backend-architecture/0-layered-architecture.md)
* [Dependency Injection in FastAPI](../backend-architecture/1-dependency-injection.md)

To get started on Phase 2, create a new branch named `phase2-services` and collaborate on it. If you and your partner work together with pair programming, working on this branch together is fine. If you are working async, start your own separate branches and be sure both of you attempt to complete this phase independently.

By the end of Phase 2, you should be able to use the `/docs` UI to complete the stories of this exercise from each user's perspective. Of importance, you should also be able to follow Cai's stories _directly_ in the web browser and be presented with plaintext or redirected to another URL by visiting the shortened URL. Finally, visit tracking and link expiration implementation is left as a challenge for extra credit.

Phase 2 should have `pytest` integration tests cover Sue Sharer and Cai Clicker's stories. You should also write unit tests that cover Sue Sharer and Cai Clicker's stories. See the [introduction to testing](../backend-architecture/2-testing.md) reading for more guidance on testing. Testing Amy's stories is left as an extra credit opportunity.

### Implementation Extra Credit

* 1 point of extra credit for integration testing and unit testing Amy's stories
* 1 point of extra credit for implementing click tracking in a way that's demonstrable and unit tested
* 1 points of extra credit for successfully implementing resource experiation in a way that's demonstrable and unit tested (hint: you'll need to find a way to cleverly simulate the passage of time by patching or mocking...)

### Phase 2: CI/CD in Production

Let's deploy your backend API to the UNC Kubernetes/OKD cluster! Then you can share snippets and redirects with your friends.

The steps we follow will be very similar to the tutorial you worked through in class on [Monday, February 17th](https://comp423-26s.github.io/resources/backend-architecture/3-ci-cd/). The general overview is:

1. Setup Continuous Integration with a GitHub Action
2. Setup a Cloud Deployment on OKD
3. Setup Continuous Deployment from GitHub Action to OKD

#### Setting up Continuous Integration with a Github Action

You will want your GitHub Action established on your `main` branch as that is where the CI/CD pipeline will run. **Only one team member should complete this sequence of steps, so coordinate as to who that will be to avoid conflicts. We recommend doing this together, if possible! This is valuable infrastructure to understand how to stand-up and what the implications are. If you do not do it together, and your team mate completes these steps, be sure to read through and check your understanding along the way.** ==Switch to your `main` branch.==

GitHub actions run in containers and will need to have your project's dependencies installed, including `pytest`. Those dependencies are in `requirements.txt`, but you may not have added `pytest` to it yet. ==Be sure `pytest` is in your `requirements.txt` pinned to the current version (as of this writing is `8.3.4`).==

Add a file named `.github/workflows/cicd.yml` to your project with the following contents:

~~~yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  ci:
    name: "Continuous Integration"
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.13
        uses: actions/setup-python@v3
        with:
          python-version: "3.13"

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Validation - pytest
        env:
          PYTHONPATH: .
        run: pytest
~~~

At this point, you are only defining the CI job. This file will be extended to perform the CD job soon.

Go ahead and create a commit on `main` and push this to your repository. Open your repository on GitHub and go to your Actions tab to see that the job runs. If you have no tests merged into your `main` branch yet then the `pytest` job will fail, which is expected. You can continue on.

#### Creating a Ruleset for Continuous Integration

Go to your repository's Settings tab > Rules > Rulesets > New ruleset. Create a Ruleset with the following settings:

* Name: `main`
* Enforcement status: Active
* Targets > Add Target > Include the Default Branch
* Checked Rules:
    * Restrict creations
    * Restrict deletions
    * Require a pull request before merging
        * Required approvals: 0
    * Require status checks to pass ==**This is CI!**==
        * Require branches to be up to date before merging (check)
        * Status checks that are required: Add checks
            * Search for "Continuous Integration" and check it. This is the job in the GitHub action you set up above! This is where your `pytest`s run. 
    * Block force pushes

Save changes. This is a slightly more sophisticated branch ruleset that you have seen prior. Namely, it will require us to use Pull Requests to merge into main. Additionally, before merging, your branches will need to successfully pass your automated tests. This is fundamentally important and characteristic of what continuous integration _is_.

#### Creating a Pull Request

Let's test this Ruleset by creating a Pull Request. In your GitHub Repository, navigate to the Pull Request tab and click **New Pull Request**. For the base, be sure your team's repository is targetted and select the `main` branch. For the compare branch, select your Phase II branch. You should see the commit history and changes between `main` and your Phase II branch here. Click **Create Pull Request**.

For the title, add a descriptive title along the lines of "Phase II Milestone: Implementation" and a meaningful description that describes what you've done in Phase II in a few sentences. Additionally, mention the "verification steps" of additional tests added with `pytest`. Then click **Create pull request.** 

After creating the PR, you will see your history of commits and you should see a message indicating "Some checks haven't completed yet" with "Continuous Integration". Assuming your tests all pass `pytest`, you will now see a button to merge your branch into `main`. ==Wait to do so, for now.== If you accidentally do merge, you will want to follow the steps below for what to do after successfully merging and let your team mate know they'll need to do the same.

#### Adding OKD/Kubernetes' `oc` Tool to the Dev Container

To setup and manage your Kubernetes/OKD cloud project from your dev container, we need to download and install the `oc` program onto your image. For the CI/CD Tutorial, this was automatically setup for you. In your project, one of you will need to add this additional configuration and push to your Phase 2 branch (or a new branch if you accidentally already merged).

If only one of you completed the prior steps alone, our suggestion is to have the other complete these steps. Like before, both of you should understand what is happening in this sequence. Here we need some additional steps taken after our dev container is created. To add these steps, we'll create a bash shell script in the `.devcontainer` directory named `post-create.sh`. A shell script is just a sequence of commands like those you could type into a terminal.

~~~bash title=".devcontainer/post-create.sh"
# Install `oc` CLI tool
arch="$(arch)"
case "$arch" in 
    x86_64) export TARGET='' ;; 
    aarch64) export TARGET='arm64-' ;; 
esac
wget -O /tmp/oc.tgz "https://github.com/okd-project/okd/releases/download/4.15.0-0.okd-2024-03-10-010116/openshift-client-linux-${TARGET}4.15.0-0.okd-2024-03-10-010116.tar.gz"
pushd /tmp
tar -xvzf oc.tgz
sudo mv oc /usr/bin/oc
rm kubectl oc.tgz README.md
popd

# Install Python Packages
pip install --upgrade pip
pip install -r requirements.txt
~~~

The first set of commands downloads the correct `oc` package (`x86_64` is for Intel/AMD-based CPUs and `aarch64` is for Mac M-family chips). The second set of commands installs your `python` packages.

After creating this file, we need to replace the current `postCreateCommand` in `devcontainer.json` to run this script instead. Open up `.devcontainer/devcontainer.json` and change the `postCreateCommand`'s assigned string to be `"bash .devcontainer/post-create.sh"` (instead of the `pip` command). Save this file and if you are prompted to rebuild the dev container, accept. If you are not prompted, be sure you saved and then use the Code Command Palatte to run "Rebuild Container."

After rebuilding, you should be able to run `oc version` and see client version `4.15.0...`. Congrats, you have successfully added the `oc` tool to your dev container setup!

#### Adding a production `Dockerfile`

When your project builds in production on OKD it will produce a Docker image. We will control the steps to produce this image using a `Dockerfile`, as explored earlier in the course. Add a new file to the root directory of your project named `Dockerfile` with the following contents:

~~~Dockerfile title="Dockerfile"
# Dockerfile for Production Build
# Use the official Python 3.13 image as the base image.
FROM python:3.13

# Set the working directory in the container.
WORKDIR /app

# Copy requirements file to the container.
# This file should list all Python dependencies.
COPY ./requirements.txt /app/requirements.txt

# Install the Python dependencies.
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code.
COPY . /app

# Expose port 8080 which uvicorn will run on.
EXPOSE 8080

# Command to run FastAPI in production mode.
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8080"]
~~~

This is a good point to add the configuration changes you just made to a new commit, push it to your Phase 2 branch, or another branch if you already merged.

#### Merging your PRs and Continuing Work

We are going to recommend using the **Squash and Merge** strategy of merging your PRs into `main` moving forward in this project. Pull up the PR for your Phase 2 changes and look for the green button. If it does not say "Squash and Merge", click the down triangle on the button and select **Squash and merge**. Go ahead and merge. Give the commit message line and extended description a meaningful message. Don't delete the branch after merging, leave it for posterity's sake in this project.

Back in your dev container, and your team mates, you will want to switch to `main` and then pull the changes from your repo. If you use `git log -1` you should see the squashed and merged commit. Additionally, you should be able to run `pytest` and see your passing tests. Woo!

Generally, when working with Pull Requests (PRs), this is your workflow:

1. Create a branch locally, push the branch to GitHub
2. Create a Pull Request (PR) on GitHub (select your team's repository's `main` branch as target)
3. Once ready to merge, merge via Squash and Merge and Fill in Commit message/Message
4. Click Confirm
5. In you and your team mates' dev container: switch to `main` and pull.

If you haven't followed these steps for your Phase 2 branch, now is a good time to go ahead and do so such that your tests and latest routes are on the `main` branch before we go to deploy.

Additionally, if you make additional changes or fixes to your implementation following deployment, just create new branches, give them meaningful names, be sure your tests cover your changes, and continue on following this process.

Soon we will see how Code Review plays into this process in engineering teams, but for now we can forego the code review process.

#### Manually Deploying your Project to OKD/Kubernetes

Both members of the team will deploy the exercise to their respective OKD namespaces. This ensures both of you have additional experience setting up the pieces and seeing how they come together. You will want to be sure you and your partner have completed the steps above. Your local dev container should be on `main`, now with all of your Phase 2 changes merged, and your dev container rebuilt such that `oc version` succeeds.

To work with UNC's OKD/Kubernetes cluster, you need to be on Eduroam or [VPN'ed in](https://ccinfo.unc.edu/start-here/secure-access-on-and-off-campus/).

Login to OKD here: <https://console.apps.unc.edu>

Get your `oc` login command by clicking your name in the top right and navigating to copy login command. Click display token and then copy the `oc login --token=...` line and paste it into your dev container's Terminal. Try running the `oc project` command to see your OKD/Kubernetes project selected (`comp590-140-26sp-<your-onyen>`).

##### Setup a Fine-grained Personal Access Token

In the CI/CD Tutorial we used a classic personal access token with wide ranging access to read your repositories on GitHub. For this project, let's use the newer style Fine-grained token that gives the token holder permission to read only your EX01 repository. The production setup will be given this token so it can access your code to build your project. To create a new one, on GitHub click your Profile > Settings > Developer settings > Personal access tokens > Fine-grained tokens > Generate new token.

* Token Name: EX01 - OKD Access - <Your Onyen>
* Resource owner: comp423-26s
* Expiration: 30 Days is Fine
* Description: Giving access to OKD to clone/access the EX01 repo.
* Repository Access:
    * Only select repositories: Select your team's repository for ex01.
* Permission:
    * Repository permissions:
        * Contents: Read-only

After clicking **Generate Token** you will be brought to a screen where it shows you, very lightly, the access token created. Copy this token to your clipboard (click the copy icon button), you will need it in the next step!

**Register your EX01 GitHub Access token as an OKD secret.** This secret will be used by your OKD BuildConfig to clone your repository into the build process. Run the following command and substitute your GitHub Username and the Access Token in the placeholders (replace the < and >'s!):

~~~bash
oc create secret generic ex01-pat \
    --from-literal=username=<your-github-username> \
    --from-literal=password=<your-github-pat>
~~~

Let's also label this secret as belonging to `app` named `ex01` so that we can easily manage it with other `ex01` related resources in the future (such as deleting everything when we move on to another project):

~~~bash
oc label secret ex01-pat app=ex01
~~~

##### Set up the App

OKD's `oc`'s `new-app` subcommand is an all-in-one command to establish a `Deployment`, `BuildConfig`, `ImageStream`, and `Service` for an application based on some common conventions. The option flags we provide below tell it our app is `Docker`-based, gives it access to the personal access token secret setup above, and because we are running this command in our current working directory `.`, `oc` is clever and looks at your `git` repository's `remote` servers to know which repository it is hooked up to.

~~~bash
oc new-app . \
    --name=ex01 \
    --source-secret=ex01-pat \
    --strategy=docker \
    --labels=app=ex01
~~~

Once this command succeeds you can try the following command to follow along with the build of your app in production:

~~~bash
oc logs -f buildconfig/ex01
~~~

This command will "follow" (thanks to `-f`), also commonly called _tail_, the output of your build in production on OKD/Kubernetes. Once the build completes you will be returned back to the command prompt, but you can also stop tailing the log with `Ctrl+C`. You can observe it following the steps of the `Dockerfile` when building your image.

Next you'll expose a secure "edge" route to your service:

~~~bash
oc create route \
    edge \
    --service=ex01 \
    --insecure-policy=Redirect
~~~

Finally, find your app's public URL on cloud apps with the following subcommand:

~~~bash
oc get route ex01
~~~

Copy the host and paste it into your browser. Try navigating to `/docs` on this host, as well. You should see your app running in production!

If you wanted to manually initiate a new build for your app based on your `main` branch, you can now do so with the following command: `oc start-build ex01`. However, we'd really like to automate deployment following a successful CI verification run and merge into the `main` branch. So let's setup continuous deployment!

#### Setting up Continuous Deployment

Now that your app is running in production, let's automate deployment on successful PR merges to `main`. You will update your GitHub Action to include a CD step.

##### Adding a Repository Secret with the URL of your OKD Build WebHook

What is a WebHook URL? It's just an API endpoint that one service (OKD/Kubernetes in our case) can expose to allow other services (GitHub) to notify them of something important. For us, we will find a secret URL OKD/Kubernetes exposes which, if we make an HTTP POST request to it, it will kick off a new build for our project in OKD/Kubernetes. We can try this from the terminal of your dev container:

First, find the secret URL:

~~~bash
oc describe bc/ex01 | grep -C 1 generic
~~~

You should see a URL that looks something like: `https://api.apps.unc.edu:6443/apis/build.openshift.io/v1/namespaces/comp590-140-26sp-ONYEN/buildconfigs/ex01/webhooks/<secret>/generic`

Next, we need to find the secret to plug into the `<secret>` part of the path. This is found in the YAML configuration for the BuildConfig (`bc`). We can filter down to it using `grep` to search for `generic` with one line of context around the matching line:

~~~bash
oc get bc ex01 -o yaml | grep -C 1 generic
~~~

You should copy the secret and paste it in place of the `<secret>` place holder in your WebHook URL. Copy this whole URL to your clipboard, we'll use it in two places.

First, let's test making a POST request to the WebHook from your dev container using the `curl` command-line utility. The `curl` program allows you to make HTTP requests from the command-line and is highly configurable:

~~~bash
curl -X POST <paste your URL with secret here>
~~~

This command will result in a message that says an invalid content-type was provided (we didn't provide any request body!) but that it is "ignoring payload and continuing with build." Woo!

You can once again follow the build you just kicked off with the command:

~~~bash
oc logs -f buildconfig/ex01
~~~

We didn't really want to start this build, we were just testing it, so you can cancel the build with the following:

~~~bash
oc get builds
oc cancel-build ex01-X
oc get builds
~~~

Replace the `X` with the number of the build you are attempting to cancel.

Let's add this secret WebHook URL to your EX01 repository as a secret your GitHub Action will be able to use. Repository > Settings > Secrets and variables > Actions > New Repository Secret:

* Name: `CD_BUILD_WEBHOOK_<ONYEN>` (substitute your ONYEN)
* Secret: Paste your secret Webhook URL found above

Save your repository secret. This will serve as a variable name in the next step.

##### Updating GitHub Action

Since both you and your team mate will both kick-off the CD step from the same GitHub Action definition, you will want to coordinate who makes the initial changes and who adds to it second. This will help avoid merge conflicts.

**If you are the first to establish continuous deployment for your production environment**, add the following to the end of your YAML file. If you are the second of your pair, just read this step to understand it, pull from `main` to get this going, and then continue to your instructions following.

{% raw %}
~~~yaml
  cd:
    name: "Continuous Deployment"
    needs: ci
    if: ${{ github.event_name == 'push' }}
    runs-on: ubuntu-latest

    steps:
      - name: Notify OKD to Build and Deploy
        run: |
          curl -X POST ${{ secrets.CD_BUILD_WEBHOOK_<ONYEN> }}
~~~
{% endraw %}

Be sure to substitute the `<ONYEN>` with yours so that it matches the name of the secret you established above.

The `cd` line should be at the same level of indentation as the `ci` entry which came in the section above. Both `ci` and `cd` are direct descendents of `jobs` based on indentation. Notice a few features of this `cd` definition:

* `needs: ci` Indicates that this job is taking a dependency on the `ci` job being successful above.
* {% raw %}`if: ${{ github.event_name == 'push' }}`{% endraw %} this conditional differentiates a push (which a merge is treated as) from a pull request build. Thus, continuous deployment is _skipped_ on Pull Requests _until_ a PR is merged to `main` (and "pushed" to `main`). This makes sense because you **do not** want to deploy to production until you merge to `main`!
* Notice in the `steps` that the command `run` is the same one you ran from the terminal with `curl`. This will trigger the WebHook.

Switch to a new branch, perhaps `cd-setup`, add these changes, make a commit, and push. Following the push, go create a Pull Request into your repository's `main` branch from the `cd-setup` branch you just pushed.

After creating the PR, you should see that your tests will run as part of the CI step and that your CD steps will be skipped, correctly, because of the `if` condition added above. Go ahead and merge this change into `main` with Squash and Merge.

After merging, go checkout your Actions tab. Take a look at how you now have a pipeline that runs: Continuous Integration followed by Continuous Deployment. These names were configured by the `name` fields in your `cicd.yaml` file in your project. You can click on either to see the process each moves through. Once the Continuous Deployment step succeeds, you should be able to check your builds to see a new build was initiated:

~~~bash
oc get builds
~~~

Once that build completes, it will deploy and you have setup a complete CI/CD workflow to a kubernetes cluster! This is something to be proud of! Now, as you make changes to your project, you will need to push to a branch, create a PR, pass all your tests, and then upon merging to `main` your work will be pushed to production automagically. This is a very real industry-grade software engineering workflow and pipeline.

Back in your dev container, switch back to `main` and pull to incorporate your squashed and merged commit.

**For the second member of the team to setup continuous deployment.** After adding your OKD project's webhook URL as a secret to your repository, your steps are as follows:

Switch to `main` in your dev container and pull your partner's merged work. Open your `.github/workflows/cicd.yaml` file and you should see their `cd` step added above. Go ahead and create a new branch, perhaps named `cd-extension`. For your part, you're just going to add one more line to the "Notify OKD to build and deploy" step:

{% raw %}
~~~yaml hl_lines="5"
    steps:
      - name: Notify OKD to Build and Deploy
        run: |
          curl -X POST ${{ secrets.CD_BUILD_WEBHOOK_<FIRST_ONYEN> }}
          curl -X POST ${{ secrets.CD_BUILD_WEBHOOK_<SECOND_ONYEN> }}
~~~
{% endraw %}

You will add the second `curl` command with your ONYEN replacing the `<SECOND_ONYEN>` placeholder. This will cause `curl` to first trigger your partner's build and then yours immediately after.

Go ahead and add this to a `git` commit on your `cd-extension` branch. Push it. Make a new PR to your repository's `main` branch. Your tests should all still pass in CI and then you should be able to squash and merge.

Upon merge, your GitHub Actions page should reflect that another worflow has begun and you can see the pipeline progress. After it completes the Continuous Deployment step, you can check your OKD production builds:

~~~bash
oc get builds
~~~

You can also tail your build:

~~~bash
oc logs -f bc/ex01
~~~

Now your Continuous Deployment step initiates builds on _both_ teammates' cloud projects! Congratulations, you have a working CI/CD pipeline.

#### Finishing up EX02

### Frequently Asked Questions

#### My Github Action is Not Running or Failing, Why?

If you do not see any attempts to build your Actions in the GitHub Actions tab of your repository, it is likely one of three reasons:

1. You have not pushed the original action definition to `main`
2. You have not initiated a Pull Request with the action definition and targetted `main`
3. Your action file is improperly named. Be sure the file extension is `.yml`

If your build is failing, there are likely one of two reasons. Open up the Action and dig into its details to see exactly where it fails by drilling in.

1. If the validation/pytest step fails because `pytest: command not found`, it is because you are missing the `pytest` dependency in `requirements.txt`. Be sure not to skip that step (search for it in the steps above!)
2. Your tests are failing in GitHub Actions for some reason. Drill in in to investigate and keep pushing additional commits to your PR until your tests are passing.

#### Should shortened URLs redirect to the URL or just display the URL?

For Cai's stories, you should be able to access the shortened URL directly in the web browser, not using `/docs` and be redirected to the URL that was shortened. You can search for FastAPI's `RedirectResponse` (and see the FAQ entry below about making sure this works in production). Note that the OpenAPI `/docs` UI will look like there is an error occuring on most redirects because it _follows_ the redirect rather than shows you the redirect response. If you see a CORS error, you're probably doing it right, but to be sure you can try accessing your URL directly (e.g. `127.0.0.1:8000/short-url`) or looking in the network tab of your browser when using the `/docs` UI. Additionally, this is a place where you should have an integration test that can confirm a redirect response is correctly being returned.

#### How should you handle hostname differences between development and production?

In development your host name is likely your localhost IP address followed by a port: `localhost:8000`. In production, your hostname will be something like `ex01-comp590-140-26sp-ONYEN.apps.unc.edu`. If your Sue routes need to produce URLs for Cai to click on, you _should not_ hard code `localhost`. Instead, you can use a dependency injection for FastAPI's `Request` object and inspect its host. Or, you can add the following helpful service to a new `url_service.py` file and inject it into a route instead. Here's the implementation:

~~~python title="url_service.py"
"""Service for creating URLs based on the current request's hostname."""

from fastapi import Request

__author__ = "Kris Jordan <kris@cs.unc.edu>"


class URLService:
    """Service for creating URLs."""

    def __init__(self, request: Request):
        """Request is dependency injected by FastAPI."""
        self._request = request

    def url_to_path(self, path: str) -> str:
        """Create a URL with the same scheme and host as the request for a given path.
        This is useful for avoiding hardcoding a host name or http/https prefix so that
        the service can be used in both production and development environments.

        In OKD, `x-forwarded-port` will be "443" for HTTPs and "80" for HTTP.

        Args:
            path: The path to create a URL for based on the current request.

        Returns:
            The created URL.
        """
        port = self._request.headers.get("x-forwarded-port") or self._request.url.port
        scheme = "https" if port == "443" else "http"
        host = self._request.headers.get(
            "x-forwarded-host"
        ) or self._request.headers.get("host")
        return f"{scheme}://{host}/{path}"
~~~

Then, from your `main.py`, you can import `URLService` and inject it into a route and use it as such:

~~~python
@app.get("/demo", ...)
def demo(url_svc: Annotated[URLService, Depends()]) -> str:
    return url_svc.url_to_path("abc123")
~~~

The result of using this service's `url_to_path` as shown above is it would return `"http://127.0.0.1:8000/abc123"` if you are running in development. In production, it will return `"https://ex01-comp590-140-26sp-ONYEN.apps.unc.edu/abc123"`, instead. If you hardcoded a hostname anywhere, you will want to either come up with your own solution or use the service above.