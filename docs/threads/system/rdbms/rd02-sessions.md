---
title: "Sessions, Transactions, and the SQLModel/SQLAlchemy ORM"
threads: ["System / RDBMS"]
authors: [Kris Jordan]
date: 2026-03-02
due: 2026-03-03
url: tbd
---

# Reading 2: 


In Reading 1, you worked directly in `psql` with the `accounts` and `activity` tables. In Reading 1B, you learned how to express those same SQL queries using SQLModel's Python API — `select()`, `.where()`, `.order_by()`, `session.get()`, and so on. In this reading, we keep the same banking domain but focus on the **Session** itself: what `commit()` does, what happens when you forget it, and how sessions fit into web applications.

## Learning Objectives

After completing this reading, you will be able to:

1. Explain what a **Session** represents.
2. Describe what `commit()` does.
3. Explain what happens if you forget to commit.
4. Explain what `refresh()` does and when it is needed.
5. Describe **transaction boundaries** in web applications.
6. Explain why **session-per-request** is a best practice.

---

## 1. What is a Session?

In lecture, we introduced a Session as a "workspace" for database operations. Formally, a Session implements the **Unit of Work** design pattern.

A **Session** is a Python object provided by SQLAlchemy that:

- **Tracks objects** you load from or add to the database (like `Account` rows represented as Python objects). It maintains an **Identity Map** (an internal registry) to ensure that if you load the same database row twice, you get the exact same Python object instance in memory.
- **Buffers changes** (inserts, updates, deletes) in memory.
- **Commits** those changes to the database as a single **transaction** when you ask it to.

Think of it like **Git**. When you use `session.add()`, it is like `git add`: you are **staging** your changes in a "Unit of Work." Nothing is permanently saved in the database until you call `session.commit()`, which is like `git commit` (however, databases updates overwrite old data and deletes are destructive).

By grouping these changes, the session ensures they are sent to the database efficiently and atomically.

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

## 2. What Does `commit()` Do?

When you call `session.commit()`, three important things happen:

1. **Flush** — The session translates all pending changes (new objects, modified attributes, deletions) into SQL statements (`INSERT`, `UPDATE`, `DELETE`) and sends them to the database.
2. **Commit the transaction** — The database finalizes the changes. After this point, the data is durably stored — it will survive a crash or power failure.
3. **Expire objects** — The session marks all tracked objects as *expired*, meaning their in-memory attributes are considered stale until explicitly refreshed.

### What if You Forget to Commit?

If you add an object to the session and never call `commit()`, the changes exist **only in memory**. When the session closes, they are discarded. The database never sees them.

```python
with Session(engine) as session:
    account = Account(owner="Ghost", email="ghost@unc.edu")
    session.add(account)
    # Oops — no commit()!
# Session closes. The account was never persisted.
```

This is one of the most common ORM bugs. If your data seems to "disappear", first verify that `commit()` is being called.

---

## 3. What Does `refresh()` Do?

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

A common pattern in services — for example, after creating activity records during a transfer:

```python
self._session.add(withdrawal)
self._session.add(deposit)
self._session.commit()

# After committing, refresh so the objects reflect DB-generated values
self._session.refresh(withdrawal)
self._session.refresh(deposit)
```

---

## 4. Transaction Boundaries

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

If anything goes wrong before `commit()` — an exception, a crash, a constraint violation — **none** of the updates take effect. The database stays exactly as it was. This is the **atomicity** guarantee of a transaction.

Notice that a single `commit()` persists all four changes (two balance updates and two activity inserts) as one atomic unit. If we credited the destination account but crashed before debiting the source, money would be created out of thin air. Transactions prevent this.

If you want a formal breakdown of why transactions are trustworthy, review the **ACID** properties introduced in Reading 1. In this reading, our focus is on how sessions and `commit()` define transaction boundaries in Python.

### What Defines a Transaction's Boundaries?

In SQLAlchemy, a transaction begins implicitly when the session first communicates with the database (e.g., on the first `session.get()` or `session.exec()`). You can see this in the `echo`'ed output of our service. It ends when you call:

- `session.commit()` — to **save** the changes, or
- `session.rollback()` — to **discard** the changes.

If the session closes without a commit, an implicit rollback occurs.

---

## 5. Session-per-Request: The Best Practice for Web Apps

In a web application, each HTTP request should get its **own** session that is created at the start of the request and closed at the end. This is the **session-per-request** pattern.

### Why Not Share a Session Across Requests?

Think about what a session tracks: loaded objects, pending changes, transaction state. If two requests share a session:

- Request A's uncommitted changes could leak into Request B's view of the data.
- A rollback in Request A could undo Request B's work.
- Thread-safety issues arise in concurrent environments.

### Implementation in FastAPI

In the demo project, `db.py` centralizes session management:

```python
# db.py

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

Services declare `SessionDI` as a constructor parameter, and FastAPI resolves it automatically:

```python
# services/account_service.py

class AccountService:
    def __init__(self, session: SessionDI) -> None:
        self._session = session

    def list_all(self) -> list[Account]:
        statement = select(Account).order_by(col(Account.id))
        return list(self._session.exec(statement).all())

    def get_by_id(self, account_id: int) -> Account | None:
        return self._session.get(Account, account_id)
```

Routes then depend on the *service*, not the session directly:

```python
# routes/account.py

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

Note: `session.commit()` runs during request handling — the endpoint will not return until the commit finishes. When using a dependency that yields (our `get_session()`), the context-manager exit (the code after `yield` that closes the session) is executed by FastAPI as the dependency teardown, which normally runs after the response is sent. See the FastAPI docs on dependencies with `yield` for details: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/.


Be aware: streaming responses delay dependency teardown until the stream completes, and background tasks run after the response is sent — so timing can vary for those cases.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| **Session** | A workspace that tracks objects and buffers changes. |
| **`commit()`** | Flushes pending changes to the DB and finalizes the transaction. |
| **Forgetting `commit()`** | Changes are discarded when the session closes. |
| **`refresh()`** | Reloads an object's attributes from the DB (needed for auto-generated values like `id` and `created_at`). |
| **ACID (review)** | Atomicity, Consistency, Isolation, Durability — review the formal definitions in Reading 1. |
| **Transaction boundaries** | Begin on first DB access, end on `commit()` or `rollback()`. |
| **Session-per-request** | Each HTTP request gets its own session — prevents cross-request data leaks. |
| **`SessionDI`** | A type alias (`Annotated[Session, Depends(get_session)]`) for concise DI in services. |

---

## Looking Ahead

Wednesday's lecture covers **testing the persistence layer**. You will learn how to write service tests against a dedicated test PostgreSQL database and run integration tests against the full FastAPI stack.
