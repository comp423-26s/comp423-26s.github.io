---
code: TK06
title: API and Service-layer Implementation (Part 2)
date: 2026-02-20
due: 2026-02-23
type: task
threads: ["System / API"]
authors: [Kris Jordan]
---

## Requirements

In the follow-on extension to [Part 1 of Task 06](./tk06_api_design.md), you will implement the following subset of three stories:

1. As Sue Sharer, I want to create a shortened URL and the ability to request a custom vanity URL, so that I can share a more meaningful link.
2. As Cai Clicker, I want to open a shortened URL by clicking its unique link, so that I am automatically redirected to the original long URL.
3. As Amy Admin, I want to see a list of all active resources (shortened URLs).

These stories are simplifications of stories you specified an API design for in Phase  Your API should still _advertise_ the more sophisticated abilities, but you can choose to ignore the additional inputs or throw an unimplemented exception if detected. If you and your partner are looking for an added challenge, implementing these capabilities is a fun, educational extension, though! Specifically, the complexities of stories from Part 1 your API was designed to handle, that **you do not need to implement in the underlying layers**, are:

1. As Sue Sharer, the optional expiration time of a shortened URL.
2. As Amy Admin, the ability to filter active resources by their view counts.

To implement these stories, you will **establish a services layer** that sits between your routes and the simple file storage implementation you wrote in previous tasks. These sevices will come together at runtime via dependency injection. 

For turn-in time saving purposes, you will only unit, integration, and end-to-end test Sue and Cai's limited stories #1 and #2. For additional practice, testing Amy's story is a good exercise, as well.

## Getting Started

You should branch off of your team's `pair-api-design` branch. Name the new branch `pair-api-implementation`. Go ahead and push this new branch name to your shared repository so you can both access it. As you progress on this assignment, you will create `wip` branches at your own direction (we recommend often!) and use the shared repository as a means for handing-off with one another.


### 1. Defining Routes in a Routing Module

You should define your final API routes in an `APIRouter` that gets included in your `main.py`'s `app`. The point of an `APIRouter` is it allows you to define _groups of routes_ together so that your app's `main` script does not grow too overwhelming. It's a divide-and-conquer approach.

Some of you noticed the `src/routes/router.py` module and its inclusion in `src/main.py` and already organized your routes in this way. If you designed your API routes in `main.py`, you can easily move them to `src/routes/router.py` by cutting, pasting, and renaming your decorators from `@app.get(...)` and `@app.post(...)` to `@router.get(...)` and `@router.post(...)`, respectively. You can [read the official documentation on `APIRouter`](https://fastapi.tiangolo.com/reference/apirouter/#fastapi.APIRouter) for additional guidance, as needed.

### 2. Establishing a Configuration Module

In any reasonably sized application that is designed for _testing_, developers and systems administrators need control over its configuration. For example, our `JSONFileIO` storage ultimately needs a string _path_ to read and write its data file to. Our little system is quite simple, so this is the only configuration it really needs, but you can imagine for more sophisticated real-world apps there are many other places where configuration needs to be controlled.

Rather than hard-coding specific string paths throughout our application's source code, we will introduce some _indirection_ to allow us to _dependency inject_ a `Config` object wherever it is useful. In doing so, we will _also_ be able to easily provide our own _test double_ for a `Config` object when writing automated tests that give us easy control over our application's configuration while testing it. This is a win-win for organization.

### 3. Establishing `config.py`

Begin by adding a file named `config.py` to your `src` directory with the following contents:

~~~python title="src/config.py" linenums="1"
"""Application configuration settings."""

from dataclasses import dataclass
from typing import Annotated, TypeAlias

from fastapi import Depends


@dataclass(frozen=True)
class Config:
    """Defines configuration values for the application.

    Attributes:
        links_path: Path to the JSON file that stores link data.
    """

    links_path: str = "data/links.json"


ConfigDI: TypeAlias = Annotated[Config, Depends()]
"""Dependency-injected Config type."""
~~~

For more information on the `@dataclass` decorator, see the [official Python documentation](https://docs.python.org/3/library/dataclasses.html). Python's `dataclass` is very similar to [Java's `record` classes](https://docs.oracle.com/en/java/javase/17/language/records.html).

You will notice we establish a `TypeAlias` for dependency injection convenience that we will make use of soon.

In the future, rather than hard-coding the `links_path` string here, we will use an _environment variable_ that is read from our process' environment to enable loading this configuration from the outside world. This is more of a production and deployment concern, though, so we will address it then. By moving this configuration into its own class, which can be dependency injected, we are achieving our goal in making it easier to substitute configuration test doubles when we get to writing tests.

### 3. Establishing `data/` directory and updating `.gitignore`

In your project, as a sibling to the `src` directory, go ahead and make a directory named `data`. You should be able to do this from the dev container's terminal after completing COMP211!

Ultimately, this is where your `Config` class is configured to read and write `links.json` once your application is running. However, we don't actually want the data in `links.json` to be committed to the repository. Otherwise, you and your partner would frequently run into merge conflicts as you collaborate asynchronously. Let's be sure `git` ignores this file by adding it to your project's `.gitignore` file. Add a section at the end that specifically ignores `data/links.json` as a path.

Finally, to ensure that this directory exists when a partner pulls or someone clones fresh in the future, add a file to the `data` directory named `.gitkeep`. Its contents will be blank. This is a conventional file name used in an otherwise empty directory to ensure the directory will be created by git. You can add this to a new commit and go ahead and make a commit.

### 4. Dependency Injection Factories and Helper Types

Your `service` layer need to compose with your `store` layer's `LinkStore` class through dependency injection. However, your `LinkStore` class' constructor requires a _path_ to the underlying data storage file (whose string file path we have established in `Config`). Thus, the dependency injection container can't automatically determine how to construct it. To get around this limitation without redesigning our `LinkStore`, we will create a _factory function_ that uses dependency injection to get a handle on `Config`.

#### 4.1 Adding `src/store/link_store_factory.py`

The following file defines a **factory function**, which is really just a plain-old function that returns an instantiated object _and_ whose parameters can all be dependency injected. Notice the single parameter is making use of the `ConfigDI` dependency injection type you setup in `config.py` above.

~~~python title="src/store/link_store_factory.py" linenums="1"
"""Dependency factory for creating link store instances."""

from pathlib import Path
from typing import Annotated, TypeAlias

from fastapi import Depends

from config import ConfigDI

from .json_file_io import JSONFileIO
from .link_store import LinkStore


def link_store_factory(config: ConfigDI) -> LinkStore:
    """Create a LinkStore wired to the configured JSON storage.

    Args:
        config: Application config containing the storage path.

    Returns:
        A LinkStore backed by the JSON file storage implementation.
    """

    storage = JSONFileIO(Path(config.links_path))
    return LinkStore(storage)


LinkStoreDI: TypeAlias = Annotated[LinkStore, Depends(link_store_factory)]
"""Dependency-injected LinkStore type."""
~~~

Reading the implementation of `link_store_factory`, notice it simply reads the `links_path` from `config` and produces a new `LinkStore` object.

Finally, notice that we are, once again, defining a `TypeAlias` for the convenience of specifying a dependency injectable `LinkStore`.

#### 4.2 Exporting the `LinkStoreDI` name from the `store` Package

As defined, if you wanted to use the `LinkStoreDI` type from our services layer, you would have to import it using the fully qualified module name it is defined in:

`from store.link_store_factory import LinkStoreDI`

However, this type makes sense to be able to import directly from the `store` package. We really want to be able to use the following import statement from other areas of our project:

`from store import LinkStoreDI`

In order to export the `LinkStoreDI` name from the `store` package, we need to add its name to the list of exported names at the package level. Python has a specific and peculiar way of doing so. If you open `src/store/__init__.py` you will see the convention.

To add `LinkStoreDI` to the list of names available at the package level, add an import statement for the `LinkStoreDI` type and then add the name to the special dunderscore variable `__all__`. This will make the name importable from the `store` package.

~~~python title="src/store/__init__.py" linenums="1"
"""Persistence layer package."""

from store.json_file_io import JSONFileIO
from store.link_store import LinkStore
from store.link_store_factory import LinkStoreDI

__all__ = ["JSONFileIO", "LinkStore", "LinkStoreDI"]
~~~

### 5. Establishing a Service Layer

In `src/services`, add a `link_service.py` module with the following starter code:

~~~python
from models import Link
from store import LinkStoreDI


class LinkService:
    def __init__(self, link_store: LinkStoreDI):
        self._link_store = link_store
~~~

Notice the `link_store` parameter is making use of the `LinkStoreDI` dependency injected type you just established.

Now that you have seen a few examples of a the `DI`-style `TypeAlias` convention we are using, go ahead and define a `TypeAlias` for `LinkService` `DI` and be sure it is exported from the `services` package.

### 6. Injecting Services in Routes

Now, _finally_, after establishing these definitions to support dependency injection, you can inject your `LinkService` service into your routes in `router.py`. First, be sure you import the `LinkServiceDI` type that you exported from `services`. Then, what do you need to do to inject a `LinkService` instance into your routes? You should be able to figure this out at this point; refer back to the readings as necessary.

## Working Together

Our recommendation for paired workflow on this assignment is:

1. Pair program on a single laptop to do the initial refactoring and getting started steps
2. Pair program to complete the initial implementation of functionality of routes. Push and fetch to sync work across your machines.
3. Split up the work of _testing_ Sue and Cai's routes individually, push to `wip` branches, review each other's code, and merge back in

## Testing Requirements

Beyond the required story implementations described in [Requirements](#requirements), there are a few testing requirements to practice unit, integration, and end-to-end tests.

For both Sue and Cai's required stories, you need to produce AAA tests following the conventions shown in the recent [reading on API testing](../threads/system/backend/2-testing-apis.md). For both routes and service methods, you should be able to demonstrate:

1. Unit Tests for the route handlers and service class methods (separate test files, well organized in `test` directory) 
2. Integration Tests for the _router, route handler, and service layers_ isolated from the _storage_ layer. There are multiple viable strategies for overriding the storage layer with a mock, but you are encouraged to experiment with FastAPI's `dependency_overrides`. Look to online resources to learn more. Try overriding `link_store_factory` via `dependency_overrides`.
3. End-to-end Tests from _router_ through _storage_. Here you will want to use `dependency_overrides` to override your `Config` to use a `pytest` provided `tmp_path` fixture. Reminder, `tmp_path` returns a path of a temporary directory location so you will need to append an actual filename. See your integration tests for `JSONFileIO` to learn more. This is still an end-to-end test because your code reads and writes from disk, the override is just making setup/teardown smoother.

For integration and end-to-end tests, you are encouraged to use VSCode's built-in debugger and test runner with debugger to step through a test line-by-line, to convince yourself of your testing subject's scope and convincing yourself you have isolated the correct targets.
