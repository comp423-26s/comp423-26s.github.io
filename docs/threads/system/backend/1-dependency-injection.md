---
code: RD17
title: "Dependency Injection"
date: 2026-02-16
due: 2026-02-17
type:  reading
threads: ["System / Backend"]
authors: ["Kris Jordan"]
---

# 1. Introduction to Dependency Injection in FastAPI

## What is Dependency Injection?

**Dependency Injection (DI)** is a widely used design pattern that promotes modular, testable, and maintainable code. It is a **core principle** in many modern application frameworks across various programming languages, including Java (Spring), Python (FastAPI), and TypeScript (Angular). The primary idea behind DI is instead of _you_ constructing dependencies _inside_ a function or class body, you declare them as _special parameters_. When the application framework calls your function, such as a route, its DI system constructs the argument values behind the scenes and "injects" them as arguments. This process is called **dependency injection**.

This concept plays a role in modern **layered architectures** like as we are exploring in this course. Dependency Injection provides a **clean, structured way** to introduce and manage dependencies between layers, keeping them **loosely coupled** and testable. We will introduce a **business logic services layer** that encapsulates domain-specific logic and separates it from the **routing layer** (which handles HTTP requests and responses). The services layer is _dependency injected_ into the routing layer.

### Why Use Dependency Injection?

Dependency Injection helps solve common software design challenges, making applications:

- **More Maintainable**: By loosely coupling dependencies between parts of a system, changes in one part of the application don’t require modifying other parts. Loosely coupled components make it easier to replace or upgrade individual parts of a system without affecting the rest. This reduces the risk of unintended side effects and promotes a more modular and extensible architecture.
- **Easier to Test**: With DI, dependencies can be replaced with mock implementations, making unit tests isolated and reliable.
- **More Flexible**: By programming to an interface rather than a concrete implementation, different implementations of a dependency can be injected dynamically, allowing for easy configuration changes.
- **Reduces Code Duplication**: Centralizing dependency management prevents repeated instantiation of services throughout the codebase.

You’ve actually already encountered DI in FastAPI! Every time a request includes **path parameters, query parameters, or request bodies**... where did the argument values come from? FastAPI injected them into your route handlers automatically! Now, let’s take this one step further: what if we wanted to inject a **custom service** into our application to handle business logic?

## How Does Dependency Injection Work in FastAPI Routing?

When a request is received in a FastAPI application, the following steps occur:

1. **Request Routing**: FastAPI matches the incoming request's URL and HTTP method to the appropriate route handler function.
2. **Dependency Resolution**: Before calling the route function, FastAPI checks for any declared dependencies using `Depends()`. It determines what dependencies are needed and resolves how to instantiate them in a correct order. An injected dependency may have its own injected dependencies that need to be resolved and instantiated first!
3. **Dependency Instantiation**: If a dependency is a class or function, FastAPI instantiates it (if needed) and injects it into the route function.
4. **Function Execution**: The route function is called with the injected dependencies passed in as arguments to the routed function's parameters.

## Tutorial: Dependency Injection in FastAPI

To follow along with this quick tutorial on dependency injection, from your host machine's terminal clone the course FastAPI Tutorial repository again, but name the cloned directory `di-tutorial`:

~~~bash
git clone https://github.com/comp423-26s/fastapi-tutorial di-tutorial
~~~

The last argument of `di-tutorial` is what causes `git` to clone to a specific directory name on your machine.

!!! info "GitHub's `gh` CLI Program"

    Now that you are comfortable with fundamental `git` commands, you may want to install GitHub's `gh` tool on your host machine. Instructions here: <https://cli.github.com>

    The `gh` tool allows you to interact with [GitHub's REST API](https://docs.github.com/en/rest?apiVersion=2022-11-28) from your command line. You can do things like [create new GitHub repositories](https://cli.github.com/manual/gh_repo_create), [list issues](https://cli.github.com/manual/gh_issue_list), and nearly anything you can do from the GitHub web page.

    Once you have `gh`, you can achieve the clone command above with:

    ~~~bash
    gh repo clone comp423-26s/fastapi-tutorial di-tutorial
    ~~~

Open the repo directory in VS Code and then open the repo in a **Dev Container**.

### Step 1: Defining Models

Let's implement a Rock, Paper, Scissors API! Create a new file in the project's root directory named `models.py`. We'll define our Pydantic data models here. Review the code below and then copy it into `models.py`:

~~~python title="models.py"
from enum import Enum
from datetime import datetime
from typing import Annotated, TypeAlias
from pydantic import BaseModel, Field


class Choice(str, Enum):
    rock = "rock"
    paper = "paper"
    scissors = "scissors"


ChoiceField: TypeAlias = Annotated[
    Choice,
    Field(
        description="Choice of rock, paper, or scissors.",
        examples=["rock", "paper", "scissors"],
    ),
]


class GamePlay(BaseModel):
    user_choice: ChoiceField


class GameResult(BaseModel):
    timestamp: Annotated[datetime, Field(description="When the game was played.")]
    user_choice: ChoiceField
    api_choice: ChoiceField
    user_wins: Annotated[bool, Field(description="Did the user win the game?")]
~~~

!!! note "Using a `TypeAlias` for repeated type annotations"

    Notice `ChoiceField` is defined as a `TypeAlias` for the annotated type of `Choice` such that it contains the `Field` information with an API description.
    
    When you find an annotated type is repeated in multiple places in your Pydantic models or FastAPI routes, using a `TypeAlias` to cut down on the repetition and make the code more readable is a best practice.

In Python, a **protocol** is similar to an interface in Java. It defines a contract that a class must follow without enforcing inheritance. This allows for better flexibility and testability.

### Step 2: Defining a `Game` Service

Now let's define a service class that handles the serious "business logic" of rock paper scissors. Review the contents below and copy the contents to a new file named `services.py`:

~~~python title="services.py"
from datetime import datetime
from random import choice as random_choice
from models import GamePlay, GameResult, Choice


class GameService:
    """Service for processing game plays.

    This class provides functionality to simulate a game between a user and the API.
    """

    def play(self, gameplay: GamePlay) -> GameResult:
        """Play a game round.

        Args:
            gameplay (GamePlay): An object encapsulating the user's choice.

        Returns:
            GameResult: The outcome of the game including user and API choices, and win flag.
        """
        api_choice: Choice = self._random_choice()

        return GameResult(
            timestamp=datetime.now(),
            user_choice=gameplay.user_choice,
            api_choice=api_choice,
            user_wins=self._does_user_win(gameplay.user_choice, api_choice),
        )

    def _random_choice(self) -> Choice:
        """Select a random choice for the API.

        Returns:
            Choice: A randomly chosen game option.
        """
        return random_choice(list(Choice))

    def _does_user_win(self, user_choice: Choice, api_choice: Choice) -> bool:
        """Determine if the user wins based on choices.

        Args:
            user_choice (Choice): The user's chosen option.
            api_choice (Choice): The API's chosen option.

        Returns:
            bool: True if the user wins, False otherwise.
        """
        result: tuple[Choice, Choice] = (user_choice, api_choice)
        winning_results: set[tuple[Choice, Choice]] = {
            (Choice.rock, Choice.scissors),
            (Choice.paper, Choice.rock),
            (Choice.scissors, Choice.paper),
        }
        return result in winning_results
~~~

Notice that this `services.py` module knows **nothing** about HTTP or FastAPI. Its imports are data models and some library functionality for randomization. This is just plain-old Python! This is the "core" logic of our little app, though, and you can easily imagine how writing unit tests for it would be straightforward.

### Step 3: Establishing a FastAPI Route to Play the Game!

Now that we have a service defined, how do we add a route that uses dependency injection to utilize it? Similar to how we declare parameters of routes that are populated by dynamic `Path` parts, `Query` parameters, or `Body` payloads.

!!! question "What HTTP method would _you_ choose for the game playing REST API endpoint?"

    We will model playing a round of this game with a `POST` method. Even though we are not (yet) storing a history of games or _creating_ anything, playing a game is *not* idempotent: we get back a new result each time we play. Not only do the `api_choice` and `user_wins` fields update, the `timestamp` reflects the latest game play.

#### Starting Without Dependency Injection

Update your `main.py` file to reflect the following. **Note: this example does not yet rely upon dependency injection! We will refactor this to make use of dependency injection next.**

~~~python title="main.py" linenums="1" hl_lines="18 19"
"""FastAPI main entrypoint file."""

from typing import Annotated, TypeAlias
from fastapi import FastAPI, Body, Depends
from models import GamePlay, GameResult
from services import GameService

app = FastAPI()


@app.post("/play")
def play(
    user_choice: Annotated[
        GamePlay,
        Body(description="User's choice of rock, paper, or scissors."),
    ],
) -> GameResult:
    # Here we construct a GameService *without* dependency injection...
    game_svc: GameService = GameService() # (1)!
    return game_svc.play(user_choice)
~~~

1. Notice that fully _inside the body_ of this function is where we declare a local variable of type `GameService` and construct it. If we later wanted to use a different object, which conformed to the interface `GameService` implements, how would we do so? We couldn't without changing this source code! Being able to swap out implementations is very useful in one common software engineering practice we will soon embrace: unit testing. In unit testing, to isolate the behavior of a single function, dependency injection gives you the ability to substitute fake dependencies in such that you are _only_ testing the unit(s) of code you care about.

!!! question "Check for understanding: Why is line 19 problematic? Why do we want to use dependency injection instead?"

    Try to answer this question for yourself before clicking the annotation symbol at the end of line 19 to reveal the answer.

#### Refactor to Dependency Injection

The updated definition of the `play` function provides an example with FastAPI's dependency injection utilized:

~~~python title="main.py" linenums="11" hl_lines="7"
@app.post("/play")
def play(
    user_choice: Annotated[
        GamePlay,
        Body(description="User's choice of rock, paper, or scissors."),
    ],
    game_svc: Annotated[GameService, Depends()],
) -> GameResult:
    return game_svc.play(user_choice)
~~~

Be sure to run the FastAPI server and try out the route from the OpenAPI `/docs` user interface!

Notice on line 17 we added an additional parameter to the `play` function definition. Its type is `Annotated[GameService, Depends()]`. The `Depends()` call is what declaratively signals to FastAPI this is a dependency injected parameter. How does it know to construct an instance of `GameService`? Because it's annotating the _type_ `GameService`. 

There are other ways of using `Depends`, too, like giving it a factory function and specifying the construction elsewhere. You can also specify the annotated type to be a `Protocol` (similar to a Java interface) and giving a concrete classname as an argument to `Depends`. That's how COMP301 should have taught you to approach a similar problem. However, we will adhere to a software engineering goal: don't overengineer until you have good reason to!

**This is dependency injection!** There is a HUGE win here: your dependency is now a parameter passed in, or _injected_, from the outside. It is not hardwired in to the route body. Thus, if you wanted to _unit test_ this function, you could easily supply a mock instance of a `GameService` and isolate the function's behavior. That said, this example is so trivial that the notion of isolating it for a unit test is a bit silly. 

### Step 4. Adding Functionality

Let's record a history of games played since the service was last restarted. We will use global module memory for this, but realize this is only a stopgap solution until we learn more about data persistence.

~~~python title="services.py" hl_lines="3-4 22-36"
# ... the import statements above remain the same ...

# This is *NOT* a database, just a hack for now...
_db: list[GameResult] = []

class GameService:
    """Service for processing game plays.

    This class provides functionality to simulate a game between a user and the API.
    """

    def play(self, gameplay: GamePlay) -> GameResult:
        """Play a game round.

        Args:
            gameplay (GamePlay): An object encapsulating the user's choice.

        Returns:
            GameResult: The outcome of the game including user and API choices, and win flag.
        """
        api_choice: Choice = self._random_choice()
        result = GameResult(
            timestamp=datetime.now(),
            user_choice=gameplay.user_choice,
            api_choice=api_choice,
            user_wins=self._does_user_win(gameplay.user_choice, api_choice),
        )
        _db.append(result)
        return result

    def get_results(self) -> list[GameResult]:
        """Get all game results.

        Returns:
            list[GameResult]: A list of all game results.
        """
        return _db

    # ... the "private" helper methods remain the same ...
~~~

Notice, we are using a simple global variable in the module to store results. Why not use an instance variable in the `GameService`? FastAPI's dependency injection system constructs a new instance of `GameService` on each request. With a little more effort we could get around this with something like the _singleton_ design pattern, to ensure only one instance of `GameService` is shared across all requests, but that's beyond the scope of this tutorial.

Let's add a route for listing the history of games played to `main.py`.

~~~python title="main.py"
@app.get("/results")
def log(game_svc: Annotated[GameService, Depends()]) -> list[GameResult]:
    return game_svc.get_results()
~~~

After saving, your FastAPI server reloads so global memory is cleared. Try playing a few games and then trying out your `/results` route. You can access it both from the `/docs` UI as well as from the browser directly, since the route's method is `GET`.

#### Cleaning Up the Types

There's one last minor tweak to make to help clean this up. You will find this useful as you write many routes which depend on the same service. Let's use a `TypeAlias` for our dependency injected `GameService` rather than repeat this annotated type everywhere. Try making the following changes in `main.py`:

~~~python title="main.py" linenums="1" hl_lines="3 10 19 25"
"""FastAPI main entrypoint file."""

from typing import Annotated, TypeAlias
from fastapi import FastAPI, Body, Depends
from models import GamePlay, GameResult
from services import GameService

app = FastAPI()

GameServiceDI: TypeAlias = Annotated[GameService, Depends()]


@app.post("/play")
def play(
    user_choice: Annotated[
        GamePlay,
        Body(description="User's choice of rock, paper, or scissors."),
    ],
    game_svc: GameServiceDI,
) -> GameResult:
    return game_svc.play(user_choice)


@app.get("/results")
def log(game_svc: GameServiceDI) -> list[GameResult]:
    return game_svc.get_results()
~~~

Ah, that's not only a little easier on the eyes, but since the `TypeAlias` is defined in one place we could now customize `Depends()` and have more control over how the `GameService` dependency gets injected across all of these routes. If we wanted to move toward a singleton pattern, for example, we could do so here.

## The Power of Dependency Injection in FastAPI

Congratulations on completing a first foray into dependency injection (DI) in FastAPI—starting from its core principles and working through a hands-on example with a Rock, Paper, Scissors. You’ve now seen how DI promotes modularity, testability, and maintainability in your applications. Instead of hardwiring dependencies, we leveraged FastAPI's `Depends()` function to keep our code clean and flexible.

Through this tutorial, you've learned how to:

* Define business logic services that remain independent of the HTTP framework.
* Use FastAPI’s DI system to inject dependencies in a structured way.
* Improve testability by allowing easy substitution of dependencies.
* Reduce code duplication and enhance maintainability.

In time, you will learn some more advanced uses of DI in FastAPI:

* Services which inject other services into their constructors. This works just like you'd expect, but still feels magical! Since our services will ultimately depend on a database layer, we will inject the database dependencies into the service.
* A nicer way of declaring routes which have many query parameters using `Depends`. [Read more here](https://fastapi.tiangolo.com/tutorial/dependencies/#what-is-dependency-injection).
* Singleton dependencies which have only one instance shared across all requests.

By adopting dependency injection, you're setting yourself up for scalable and maintainable application development. Whether you're working on a small personal project or a large-scale system, mastering DI ensures that your code remains clean and modular.