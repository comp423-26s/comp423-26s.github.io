---
code: RD22
title: "Engines, Sessions, and Transactions in SQLModel/SQLAlchemy"
threads: ["System / RDBMS"]
authors: [Kris Jordan]
date: 2026-03-02
due: 2026-03-03
---

In the first database reading, you worked directly in `psql` with the `accounts` and `activity` tables. In the previous reading, you learned how to express those same SQL queries using SQLModel's Python API, such as `select()`, `.where()`, `.order_by()`, `session.get()`, and so on. In this reading, we keep the same banking domain but zoom out one level further, starting with the **Engine** that connects your Python app to PostgreSQL, then the **Session** that manages a single unit of work, and finally how all of it fits together in our development environment with Docker Compose.

## Learning Objectives

After completing this reading, you will be able to:

1. Explain what an **Engine** is and its role in database connectivity.
2. Describe the relationship between an Engine and a Session.
3. Explain what a **Session** represents.
4. Describe what `commit()` does.
5. Explain what happens if you forget to commit.
6. Explain what `refresh()` does and when it is needed.
7. Describe **transaction boundaries** in web applications.
8. Explain why **session-per-request** is a best practice.
9. Explain how Docker Compose service names become hostnames in a database connection string.
10. Describe what a Docker named volume provides for database persistence.

---

## 1. The `Engine` is Your App's Connection to the Database

Before a session can read or write anything, it needs a live **connection** to the database. That connection is managed by the **Engine**.

An Engine is a long-lived Python object, created once per application process, that:

- Holds the **database connection URL**: the address, credentials, and database name needed to reach PostgreSQL.
- Manages a **connection pool**: a set of open TCP connections held ready for reuse across requests. Opening a brand-new TCP connection to PostgreSQL on every HTTP request would be expensive; pooling lets sessions borrow and return connections cheaply.

In the demo project, the engine is defined in `db.py`:

```python title="db.py"
from sqlmodel import create_engine

POSTGRES_URL = "postgresql://postgres:mysecretpassword@db:5432/bank"

engine = create_engine(POSTGRES_URL, echo=True)
```

The connection URL encodes everything SQLAlchemy needs to find and authenticate with the database:

| Segment | Value | Meaning |
|---------|-------|---------|
| protocol | `postgresql` | Which database driver to use |
| user | `postgres` | Database login username |
| password | `mysecretpassword` | Database login password |
| host | `db` | Hostname of the PostgreSQL server |
| port | `5432` | PostgreSQL's default port |
| database | `bank` | Which database to select on connect |

We will cover *why* the host is named `db`, not an IP address,  when we look at Docker Compose in Section 7. The short answer: Docker Compose gives each service a hostname matching its service name, so the `db` service is reachable as `db`.

`echo=True` tells SQLAlchemy to print every SQL statement it generates to stdout. While learning, this is invaluable: you can watch the exact SQL your Python code triggers for each `session.exec()`, `session.add()`, or `session.commit()`. Set `echo=False` (or omit it) in production.

### The Engine's Relationship to a Session

The Engine and Session are two distinct layers with very different lifetimes:

| | **Engine** | **Session** |
|-|-----------|------------|
| **Lifetime** | One per application process: created at startup, lives until shutdown | One per HTTP request: created when the request arrives, closed when it is handled |
| **Responsibility** | *How* to talk to the database: manages TCP connections, pooling, and the database driver | *What* to persist: tracks Python objects, buffers changes, and defines a transaction boundary |

When you write `Session(engine)`, the Session borrows a connection from the Engine's pool for the duration of its work. When the session closes, the connection is returned to the pool, ready for the next request. This is why the Engine is created once (at import time in `db.py`) while a new Session is created for every request.

---

## 2. What is a Session?

In lecture, we introduced a Session as a "workspace" for database operations. Formally, a Session implements the **Unit of Work** design pattern.

A **Session** is a Python object provided by SQLAlchemy that:

- **Tracks objects** you load from or add to the database (like `Account` rows represented as Python objects). It maintains an **Identity Map** (an internal registry) to ensure that if you load the same database row twice, you get the exact same Python object instance in memory.
- **Buffers changes** (inserts, updates, deletes) in memory.
- **Commits** those changes to the database as a single **transaction** when you ask it to.

Think of it as conceptually similar to working with **`git`**. When you use `session.add()`, it is like `git add`: you are **staging** your changes in a "Unit of Work." Nothing is permanently saved in the database until you call `session.commit()`, which is like `git commit`, however, as you know, database updates overwrite data and deletes are destructive, unlike `git`'s nominally immutable history.

By grouping these changes, the session ensures they are sent to the database efficiently and persisted atomically.

```python
from sqlmodel import Session

with Session(engine) as session:
    # Start working...
    account = Account(owner="SpongeBob", email="spongebob@unc.edu", balance=500)
    session.add(account)        # Staged, not yet in the database
    session.commit()            # Now it is persisted in the database
```

### The Session Lifecycle

```
┌──────────────┐
│ Create       │  with Session(engine) as session
│ Session      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Work         │  .add(), .get(), .exec(), modify attributes
│ (in memory)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Commit       │  .commit() → SQL sent to DB, transaction finalized
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Close        │  end of `with` block
└──────────────┘
```

---

## 3. What Does `commit()` Do?

When you call `session.commit()`, three important things happen:

1. **Flush**: The session translates all pending changes (new objects, modified attributes, deletions) into SQL statements (`INSERT`, `UPDATE`, `DELETE`) and sends them to the database.
2. **Commit the transaction**: The database finalizes the changes. After this point, the data is durably stored and will survive a crash or power failure.
3. **Expire objects**: The session marks all tracked objects as *expired*, meaning their in-memory attributes are considered stale until explicitly refreshed.

### What if You Forget to Commit?

If you add an object to the session and never call `commit()`, the changes exist **only in memory**. When the session closes, they are discarded. The database never sees them.

```python
with Session(engine) as session:
    account = Account(owner="Ghost", email="ghost@unc.edu")
    session.add(account)
    # Oops! No commit()!
# Session closes. The account was never persisted.
```

This is one of the most common ORM bugs. If your data does not seem to "save", first verify that `commit()` is being called.

---

## 4. What Does `refresh()` Do?

After `commit()`, SQLAlchemy marks tracked objects as *expired*. Their Python attributes may be stale because the database may have assigned auto-generated values (like a `SERIAL` primary key that gets assigned an integer value or a `DEFAULT CURRENT_TIMESTAMP` which denotes the time a row was inserted into the table).

Calling `session.refresh(obj)` issues a `SELECT` to reload the object's attributes from the database:

```python
account = Account(owner="SpongeBob", email="spongebob@unc.edu")
session.add(account)
session.commit()

# At this point, account.id is expired / not yet loaded
session.refresh(account)

print(account.id)  # Now contains the auto-generated ID, e.g. 1
```

### When Do You Need `refresh()`?

| Situation | Need `refresh()`? |
|-----------|-------------------|
| After `commit()` and you need auto-generated fields (e.g., `id`, `created_at`) | **Yes** |
| After `commit()` and you are done with the object | No |
| After modifying an object but before committing | No |
| After calling `session.get()` (data is fresh from DB) | No |

For example, a common pattern in services after creating activity records during a transfer:

```python
self._session.add(withdrawal)
self._session.add(deposit)
self._session.commit()

# After committing, refresh so the objects reflect DB-generated values
self._session.refresh(withdrawal)
self._session.refresh(deposit)
```

---

## 5. Transaction Boundaries

A **transaction** is a group of database operations that succeed or fail **as a unit**. The classic example from our banking domain: transferring money between two accounts.

In our demo project, the `ActivityService.transfer()` method demonstrates this:

```python
def transfer(self, from_account: Account, to_account: Account, amount: int):
    # --- Guard clauses ---
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if from_account.balance < amount:
        raise ValueError("Insufficient funds.")

    # --- Mutate balances ---
    from_account.balance -= amount
    to_account.balance += amount

    # --- Create ledger entries ---
    withdrawal = Activity(
        account_id=from_account.id,
        activity_type=ActivityType.WD,
        amount=amount,
    )
    deposit = Activity(
        account_id=to_account.id,
        activity_type=ActivityType.DEP,
        amount=amount,
    )

    self._session.add(from_account)
    self._session.add(to_account)
    self._session.add(withdrawal)
    self._session.add(deposit)
    self._session.commit()  # All four changes happen atomically

    self._session.refresh(withdrawal)
    self._session.refresh(deposit)
    return withdrawal, deposit
```

If anything goes wrong before `commit()`, such as an exception, a crash, or a constraint violation, **none** of the updates take effect. The database stays exactly as it was. This is the **atomicity** guarantee of a transaction.

Notice that a single `commit()` persists all four changes (two balance updates and two activity inserts) as one atomic unit. If we credited the destination account but crashed before debiting the source, money would be created out of thin air. Transactions prevent this.

If you want a formal breakdown of why transactions are trustworthy, review the **ACID** properties introduced in the first databases reading. In this reading, our focus is on how sessions and `commit()` define transaction boundaries in Python.

### What Defines a Transaction's Boundaries?

In SQLAlchemy, a transaction begins implicitly when the session first communicates with the database (e.g., on the first `session.get()` or `session.exec()`). You can see this in the `echo`'ed output of our service. It ends when you call:

- `session.commit()`: to **save** the changes, or
- `session.rollback()`: to **discard** the changes.

If the session closes without a commit, an implicit rollback occurs.

---

## 6. Session-per-Request is idiomatic in Web Apps

In a web application, each HTTP request should get its **own** session that is created at the start of the request and closed at the end. This is the **session-per-request** pattern.

### Why Not Share a Session Across Requests?

Think about what a session tracks: loaded objects, pending changes, transaction state. If two requests share a session:

- Request A's uncommitted changes could leak into Request B's view of the data.
- A rollback in Request A could undo Request B's work.
- Thread-safety issues arise in concurrent environments.

### Implementation in FastAPI

In the demo project, `db.py` centralizes session management:

```python title="db.py"
from collections.abc import Generator
from typing import Annotated, TypeAlias

from fastapi import Depends
from sqlmodel import Session, create_engine

POSTGRES_URL = "postgresql://postgres:mysecretpassword@db:5432/bank"
engine = create_engine(POSTGRES_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    """Provide a transactional database session for a single request."""
    with Session(engine) as session:
        yield session


# Convenience type alias for dependency injection.
SessionDI: TypeAlias = Annotated[Session, Depends(get_session)]
```

Services declare `SessionDI` as a constructor parameter, and FastAPI resolves it via dependency injection:

```python title="services/account_service.py"
class AccountService:
    def __init__(self, session: SessionDI) -> None:
        self._session = session

    def list_all(self) -> list[Account]:
        statement = select(Account).order_by(col(Account.id))
        return list(self._session.exec(statement).all())

    def get_by_id(self, account_id: int) -> Account | None:
        return self._session.get(Account, account_id)
```

Routes then depend on the *service*, not the session directly. In fact, routes should **know nothing** about sessions thanks to proper layering. The database is layered below the services layer and services are layered below route handlers:

```python title="routes/account.py"
@router.get("/accounts", response_model=list[Account])
def list_accounts(account_svc: AccountServiceDI) -> list[Account]:
    return account_svc.list_all()
```

When the request ends, the `with` block in `get_session()` closes the session. Each request is an isolated unit of work.

### The Pattern Visualized

```
HTTP Request arrives
      │
      ▼
  ┌────────────────────────────┐
  │ Dependency: get_session()  │  ← context-manager entered, `session` yielded
  └──────────┬─────────────────┘
           │
           ▼
       Route / Endpoint
           │
           ▼
      Service (uses session)
           │
           ▼
    service calls `session.commit()`  ← runs during request handling (client waits)
           │
           ▼
    FastAPI sends HTTP response to client
           │
           ▼
  ┌────────────────────────────┐
  │ Dependency teardown (after)│  ← `session` context manager exits, session closed
  └────────────────────────────┘
```

Note: `session.commit()` runs during request handling. The endpoint will not return until the commit finishes. When using a dependency that yields (our `get_session()`), the context-manager exit (the code after `yield` that closes the session) is executed by FastAPI as the dependency teardown, which normally runs after the response is sent. See the FastAPI docs on dependencies with `yield` for details: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/.

---

## 7. Dev Container Setup with Docker Compose

So far in this reading you have seen `POSTGRES_URL = "postgresql://postgres:mysecretpassword@db:5432/bank"` in `db.py`. We have not yet explained *where the `db` hostname comes from*, or *how PostgreSQL is running alongside your FastAPI app at all*. Let's take a look.

### Two Processes, Two Containers

Your FastAPI application and PostgreSQL database run as **two separate processes** in **two separate Docker containers**. Docker Compose defines and orchestrates both together:

```
┌─────────────────────────────┐     ┌─────────────────────────────┐
│  app container              │     │  db container               │
│  (your FastAPI app + code)  │────▶│  (PostgreSQL server)        │
│  Port 8000                  │     │  Port 5432                  │
└─────────────────────────────┘     └──────────┬──────────────────┘
                                               │
                                    ┌──────────▼──────────────────┐
                                    │  Docker Volume              │
                                    │  postgres-data              │
                                    └─────────────────────────────┘
```

Your application (FastAPI) is one process. The database (PostgreSQL) is another. They communicate over a **network connection** even though both run on the same physical machine. They talk to each other over TCP, just like in a production system.

### The `docker-compose.yml`

The demo project provides a `docker-compose.yml` at the project root that defines both services:

```yaml title=".devcontainer/docker-compose.yml"
services:
  app:
    image: mcr.microsoft.com/devcontainers/python:3.14
    command: sleep infinity
    volumes:
      - ../:/workspace
    depends_on:
      - db

  db:
    image: postgres:18
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: mysecretpassword
      POSTGRES_DB: bank
    ports:
      - "5432:5432"
    volumes:
      - orm-demo-data:/var/lib/postgresql

volumes:
  orm-demo-data:
```

There are several things to unpack here.

#### Service Names Become Hostnames

Docker Compose creates a **private virtual network** shared by all services defined in the same file. Within that network, each service is reachable by the other services **using its service name as a hostname**, no IP address is required.

The PostgreSQL service is named **`db`**. That is exactly why `db.py` uses `db` as the hostname in the connection string:

```python
POSTGRES_URL = "postgresql://postgres:mysecretpassword@db:5432/bank"
#                                                      ^^
#                       matches the service name in docker-compose.yml
```

When the `app` container connects to `db:5432`, Docker's internal DNS resolves `db` to the PostgreSQL container's IP address automatically. You never need to know or hard-code an actual IP.

!!! warning "Hard-coded credentials are for learning only"
    In a real application you would never commit a password to source control. The connection string would be assembled from environment variables or a secret manager at runtime. This is acceptable for the demo project but would be a serious security issue in production.

#### `depends_on`: Starting Order

The `app` service declares `depends_on: db`, which tells Docker Compose to start the `db` container **before** starting the `app` container. Without this, the FastAPI application might attempt a database connection before PostgreSQL has finished initializing.

#### The Named Volume

```yaml
volumes:
      - orm-demo-data:/var/lib/postgresql
```

This mounts a **named volume** called `orm-demo-data` at the path where PostgreSQL stores its data files. A named volume is managed by Docker independently of any container:

| Without a volume | With a named volume (`orm-demo-data`) |
|-----------------|--------------------------------------|
| Data lives inside the container's writable layer | Data lives in a Docker-managed volume on the host |
| Removing or rebuilding the container erases all data | Data survives container rebuilds and restarts |
| Fine for a one-off experiment | Required for any data you care about |

Run `docker volume ls` in a terminal to see the volumes Docker is tracking. After the containers have started at least once, you will see `orm-demo-data` listed there.

### Wiring It into the Dev Container

The `.devcontainer/devcontainer.json` tells VS Code to use `docker-compose.yml` to spin up the full multi-container environment instead of building a single standalone container:

```json title=".devcontainer/devcontainer.json"
{
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace"
}
```

| Key | Purpose |
|-----|---------|
| `dockerComposeFile` | Points VS Code at the Compose file instead of a single `Dockerfile` |
| `service` | Specifies which service is the dev container you work *inside* (`app`) |
| `workspaceFolder` | The directory inside the `app` container that VS Code treats as the workspace root |

When you reopen the project in a dev container, VS Code runs `docker compose up` behind the scenes, starting **both** services. PostgreSQL starts first (enforced by `depends_on`), then the app container. By the time your terminal is ready, `db:5432` is already reachable from your FastAPI code.

---

## 8. Summary

| Concept | Key Takeaway |
|---------|-------------|
| **Engine** | A long-lived object (one per app process) that holds the connection URL and manages a pool of database connections. |
| **Engine ↔ Session** | The Session borrows a connection from the Engine's pool for one unit of work, then returns it when done. |
| **Session** | A workspace that tracks objects and buffers changes. |
| **`commit()`** | Flushes pending changes to the DB and finalizes the transaction. |
| **Forgetting `commit()`** | Changes are discarded when the session closes. |
| **`refresh()`** | Reloads an object's attributes from the DB (needed for auto-generated values like `id` and `created_at`). |
| **ACID (review)** | Atomicity, Consistency, Isolation, Durability |
| **Transaction boundaries** | Begin on first DB access, end on `commit()` or `rollback()`. |
| **Session-per-request** | Each HTTP request gets its own session to prevent cross-request data leaks. |
| **`SessionDI`** | A type alias (`Annotated[Session, Depends(get_session)]`) for concise DI in services. |
| **Docker Compose** | Defines and orchestrates multiple services (e.g., `app` + `db`) as a single unit. |
| **Service name as hostname** | Docker Compose creates a private network; services reach each other by service name (`db:5432`). |
| **Named volume** | A Docker-managed volume that outlives containers which persists database data across restarts. |
| **`devcontainer.json`** | Configures VS Code to use `docker-compose.yml` and open the `app` service as the dev container. |
