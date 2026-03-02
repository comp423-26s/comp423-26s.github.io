---
title: "Querying with SQLModel"
threads: ["System / RDBMS"]
authors: [Kris Jordan]
date: 2026-03-02
due: 2026-03-03
url: tbd
---

# Querying with SQLModel

In Reading 1 you wrote raw SQL — `SELECT`, `WHERE`, `ORDER BY`, `INSERT`, `UPDATE`, and aggregate functions — directly in `psql`. In Monday's lecture you saw how **SQLModel** maps Python classes to database tables and how a **Session** sends SQL to PostgreSQL on your behalf.

This reading bridges those two worlds. For every SQL query pattern you learned in Reading 1, we show the equivalent Python code using SQLModel's query-building API. By the end, you should be able to look at a raw SQL statement and translate it to Python (and vice versa).

## Learning Objectives

After completing this reading, you will be able to:

1. Translate a `SELECT ... FROM ... WHERE` SQL query into a SQLModel `select()` statement.
2. Use `session.exec()` to run a `select()` statement and retrieve results.
3. Use `session.get()` to look up a row by primary key.
4. Apply filtering (`.where()`), sorting (`.order_by()`), and limiting (`.limit()`) to `select()` statements.
5. Use `col()` for column references in `order_by()` and `where()` clauses.
6. Translate SQL `INSERT` and `UPDATE` operations into their SQLModel equivalents using `session.add()` and attribute assignment.
7. Describe, at a high level, how aggregate queries differ from simple selects.

---

## Prerequisites: The Banking Demo Project

All examples in this reading use the **banking demo project** from lecture. The two entity classes mirror the SQL tables you created in Reading 1:

```python
# entities/account.py
class Account(SQLModel, table=True):
    __tablename__ = "accounts"

    id: int | None = Field(default=None, primary_key=True)
    owner: str
    email: str = Field(sa_column=Column(String, unique=True, nullable=False))
    balance: int = Field(default=0)
```

```python
# entities/activity.py
class Activity(SQLModel, table=True):
    __tablename__ = "activity"

    id: int | None = Field(default=None, primary_key=True)
    account_id: int = Field(foreign_key="accounts.id")
    activity_type: ActivityType
    amount: int
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime, server_default=func.now()),
    )
```

Compare these classes to the `CREATE TABLE` statements from Reading 1 — each Python field corresponds to a SQL column, and constraints like `primary_key`, `unique`, and `foreign_key` map directly to their SQL counterparts.

Throughout this reading, assume we have access to a `session` object (a `Session` from SQLModel). You will learn exactly how sessions are created and managed in Reading 2. For now, think of `session` as a connection to the database that lets you run queries and save changes.

---

## 1. The `select()` Function — Building Queries in Python

In SQL, `SELECT` is the workhorse for reading data. In SQLModel, the equivalent is the `select()` function, which returns a **statement object** that you can refine with method calls before executing.

### Anatomy of a SQLModel Query

Here is the general pattern you will see:

```python
from sqlmodel import select

statement = select(Account)               # Build the query
results = session.exec(statement).all()   # Execute and collect rows
```

This is equivalent to:

```sql
SELECT * FROM accounts;
```

The key idea: **`select()` builds the query; `session.exec()` runs it.**

Think of `select()` as assembling a SQL statement piece by piece in Python. Nothing touches the database until you call `session.exec()`. This separation is useful because you can construct complex queries programmatically before sending them.

### How `session.exec()` Returns Results

`session.exec(statement)` returns a result object. The most common ways to consume it:

| Method | Returns | Use When |
|--------|---------|----------|
| `.all()` | A list of all matching rows | You want every result |
| `.first()` | The first row, or `None` | You expect zero or one result |
| `.one()` | Exactly one row (raises if 0 or 2+) | You are certain exactly one row matches |

For example:

```python
# Get all accounts as a list
all_accounts = session.exec(select(Account)).all()

# Get the first account (or None if the table is empty)
first_account = session.exec(select(Account)).first()
```

---

## 2. Looking Up a Row by Primary Key — `session.get()`

The simplest and most common lookup is finding a row by its **primary key**. SQLModel provides a shortcut for this:

```python
account = session.get(Account, 1)
```

This is equivalent to:

```sql
SELECT * FROM accounts WHERE id = 1;
```

`session.get()` returns the object if it exists, or `None` if no row has that primary key. This is the method you will use most often when you need a specific row — for example, when a route handler receives an account ID from the URL path.

In the demo project, the `AccountService` uses this pattern:

```python
def get_by_id(self, account_id: int) -> Account | None:
    return self._session.get(Account, account_id)
```

!!! note "Why `session.get()` instead of a `select()` with `where()`?"
    `session.get()` first checks the session's **identity map** — an internal cache of objects already loaded in this session. If the object is already in memory, it returns it immediately without hitting the database. This makes it both simpler and faster for primary key lookups.

---

## 3. Filtering with `.where()` — The Python Equivalent of `WHERE`

In SQL, `WHERE` filters rows based on conditions. In SQLModel, you chain `.where()` onto a `select()` statement.

### The `col()` Helper

Before we dive into examples, a quick note on `col()`. When writing filter or sort expressions, SQLModel needs to know you are referring to a **database column**, not just a Python attribute. The `col()` function wraps a model attribute to make this explicit:

```python
from sqlmodel import col, select
```

You will see `col()` used throughout the demo project and this reading. It ensures type-safe, unambiguous column references.

### Exact Match (SQL `=`)

**SQL:**
```sql
SELECT * FROM accounts WHERE email = 'spongebob@unc.edu';
```

**SQLModel:**
```python
statement = select(Account).where(col(Account.email) == "spongebob@unc.edu")
account = session.exec(statement).first()
```

Notice the double equals `==` — this is Python's equality operator. SQLModel translates it into the SQL `=` operator behind the scenes.

### Comparison (SQL `>`, `<`, `>=`, `<=`)

**SQL:**
```sql
SELECT * FROM accounts WHERE balance > 300;
```

**SQLModel:**
```python
statement = select(Account).where(col(Account.balance) > 300)
results = session.exec(statement).all()
```

Python's comparison operators (`>`, `<`, `>=`, `<=`, `!=`) translate directly to their SQL equivalents.

### Pattern Matching (SQL `LIKE`)

**SQL:**
```sql
SELECT * FROM accounts WHERE owner LIKE 'S%';
```

**SQLModel:**
```python
statement = select(Account).where(col(Account.owner).startswith("S"))
results = session.exec(statement).all()
```

SQLModel translates `.startswith("S")` into `LIKE 'S%'`. There are also `.endswith()` and `.contains()` for other patterns:

| Python Method | SQL Equivalent |
|---------------|---------------|
| `.startswith("S")` | `LIKE 'S%'` |
| `.endswith("edu")` | `LIKE '%edu'` |
| `.contains("bob")` | `LIKE '%bob%'` |

### Filtering Activity by Account

In the demo project, `ActivityService.list_for_account()` filters activity rows for a specific account:

```python
def list_for_account(self, account: Account) -> list[Activity]:
    statement = (
        select(Activity)
        .where(col(Activity.account_id) == account.id)
        .order_by(col(Activity.id).desc())
    )
    return list(self._session.exec(statement).all())
```

This is equivalent to:

```sql
SELECT * FROM activity WHERE account_id = 1 ORDER BY id DESC;
```

---

## 4. Sorting with `.order_by()` — The Python Equivalent of `ORDER BY`

### Ascending Order (Default)

**SQL:**
```sql
SELECT * FROM accounts ORDER BY owner ASC;
```

**SQLModel:**
```python
statement = select(Account).order_by(col(Account.owner))
results = session.exec(statement).all()
```

By default, `.order_by()` sorts in **ascending** order, just like SQL's default.

### Descending Order

**SQL:**
```sql
SELECT * FROM accounts ORDER BY balance DESC;
```

**SQLModel:**
```python
statement = select(Account).order_by(col(Account.balance).desc())
results = session.exec(statement).all()
```

The `.desc()` method on a column reference produces descending order. The demo project uses this pattern in `ActivityService.list_all()`:

```python
def list_all(self) -> list[Activity]:
    statement = select(Activity).order_by(col(Activity.id).desc())
    return list(self._session.exec(statement).all())
```

### Ascending (Explicit)

If you want to be explicit about ascending order, use `.asc()`:

```python
statement = select(Account).order_by(col(Account.owner).asc())
```

---

## 5. Limiting Results with `.limit()`

**SQL:**
```sql
SELECT * FROM accounts ORDER BY balance DESC LIMIT 1;
```

**SQLModel:**
```python
statement = select(Account).order_by(col(Account.balance).desc()).limit(1)
richest = session.exec(statement).first()
```

`.limit(n)` restricts the result set to at most `n` rows, just like SQL's `LIMIT`. Combining `.order_by()` with `.limit()` is a common pattern for "top N" queries.

---

## 6. Chaining It All Together

One of the strengths of the query-building API is that you can chain clauses together. Each method returns a new statement object, so you can build up complex queries incrementally:

```python
statement = (
    select(Account)
    .where(col(Account.balance) > 100)
    .order_by(col(Account.owner).asc())
    .limit(10)
)
results = session.exec(statement).all()
```

This is equivalent to:

```sql
SELECT * FROM accounts
WHERE balance > 100
ORDER BY owner ASC
LIMIT 10;
```

The chain reads naturally from top to bottom: *select accounts, where balance is over 100, ordered by owner, limit to 10.*

### Evaluation Order

Just like in SQL, the logical evaluation order is:

1. **`select(Account)`** — choose the table
2. **`.where(...)`** — filter rows
3. **`.order_by(...)`** — sort the remaining rows
4. **`.limit(...)`** — take the first N

This mirrors the mental model from Reading 1: `FROM` → `WHERE` → `SELECT` → `ORDER BY` → `LIMIT`.

---

## 7. Inserting Data — `session.add()` Instead of `INSERT`

In SQL, you insert rows with `INSERT INTO`. In SQLModel, you create a Python object and add it to the session:

**SQL:**
```sql
INSERT INTO accounts (owner, email, balance) VALUES ('SpongeBob', 'spongebob@unc.edu', 500);
```

**SQLModel:**
```python
account = Account(owner="SpongeBob", email="spongebob@unc.edu", balance=500)
session.add(account)
session.commit()
```

Key differences from raw SQL:

- You do not specify the `id` — the database auto-generates it, just like `SERIAL` in SQL.
- `session.add()` **stages** the object. Nothing is written to the database until `session.commit()` is called. (Reading 2 covers `commit()` in depth.)
- After committing, you can call `session.refresh(account)` to load the auto-generated `id` back into the Python object.

### Adding Multiple Rows

To insert several rows at once:

```python
spongebob = Account(owner="SpongeBob", email="spongebob@unc.edu", balance=500)
squidward = Account(owner="Squidward", email="squidward@unc.edu", balance=250)
patrick = Account(owner="Patrick", email="patrick@unc.edu", balance=1000)

session.add_all([spongebob, squidward, patrick])
session.commit()
```

This is equivalent to running three `INSERT` statements in a single transaction.

---

## 8. Updating Data — Modify Attributes Instead of `UPDATE`

In SQL, you use `UPDATE ... SET` to change values. With the ORM, you modify the Python object's attributes directly:

**SQL:**
```sql
UPDATE accounts SET balance = balance + 100 WHERE id = 1;
```

**SQLModel:**
```python
account = session.get(Account, 1)
account.balance += 100
session.add(account)
session.commit()
```

The session **tracks changes** to objects it manages. When you modify `account.balance`, the session knows the attribute has changed. On `commit()`, it generates the appropriate `UPDATE` SQL.

!!! note "ORM updates vs. SQL arithmetic"
    Notice a subtle difference: the raw SQL `balance = balance + 100` tells the *database* to do the arithmetic. The ORM version reads the current value into Python, adds 100 in Python, and writes the result back. For most applications this works fine. Reading 5 discusses edge cases where this distinction matters under concurrent access.

### The Transfer Pattern

The demo project's `ActivityService.transfer()` method updates two accounts and creates two activity entries in a single transaction:

```python
from_account.balance -= amount
to_account.balance += amount

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
self._session.commit()
```

This mirrors the multi-statement SQL transaction from Reading 1:

```sql
BEGIN;
INSERT INTO activity (account_id, activity_type, amount) VALUES (1, 'WD', 200);
INSERT INTO activity (account_id, activity_type, amount) VALUES (2, 'DEP', 200);
UPDATE accounts SET balance = balance - 200 WHERE id = 1;
UPDATE accounts SET balance = balance + 200 WHERE id = 2;
COMMIT;
```

A single `session.commit()` ensures all four changes happen atomically — just like `BEGIN` / `COMMIT` in SQL.

---

## 9. Deleting Data — `session.delete()` Instead of `DELETE`

In SQL, `DELETE FROM` removes rows. In SQLModel, you pass the object to `session.delete()`:

**SQL:**
```sql
DELETE FROM activity WHERE id = 6;
```

**SQLModel:**
```python
activity = session.get(Activity, 6)
if activity:
    session.delete(activity)
    session.commit()
```

Like `add()`, the deletion is staged until `commit()` is called. If you forget to commit, the row remains in the database.

---

## 10. Selecting Specific Columns

So far, every `select()` has fetched entire objects (all columns). Sometimes you only need one or two columns.

**SQL:**
```sql
SELECT owner, balance FROM accounts;
```

**SQLModel:**
```python
statement = select(Account.owner, Account.balance)
results = session.exec(statement).all()
```

When you pass individual columns to `select()` instead of the model class, the results are **tuples** rather than model objects:

```python
for owner, balance in results:
    print(f"{owner}: ${balance}")
```

This can be more efficient when you don't need the full object, but for most service-layer code, selecting the full model (via `select(Account)`) is simpler and more maintainable.

---

## 11. Aggregates — A Brief Overview

In Reading 1 you used `COUNT(*)`, `SUM()`, and `GROUP BY` to compute summaries across rows. SQLAlchemy provides the `func` object for calling SQL functions from Python:

```python
from sqlmodel import func, select
```

### Counting Rows

**SQL:**
```sql
SELECT COUNT(*) FROM accounts;
```

**SQLModel:**
```python
statement = select(func.count()).select_from(Account)
count = session.exec(statement).one()
```

### Summing a Column

**SQL:**
```sql
SELECT SUM(balance) FROM accounts;
```

**SQLModel:**
```python
statement = select(func.sum(Account.balance))
total = session.exec(statement).one()
```

### Grouping — `GROUP BY`

**SQL:**
```sql
SELECT account_id, COUNT(*) AS num_entries
FROM activity
GROUP BY account_id
ORDER BY account_id;
```

**SQLModel:**
```python
statement = (
    select(Activity.account_id, func.count())
    .group_by(Activity.account_id)
    .order_by(Activity.account_id)
)
results = session.exec(statement).all()
```

Each result is a tuple `(account_id, count)`.

!!! note "Aggregates in practice"
    In the demo project, we don't use aggregate queries in the service layer — the endpoints return lists of objects, and any summarization happens in the frontend or in application code. But knowing how to express aggregates through the ORM is valuable when you need database-level computation for performance (e.g., counting thousands of rows is much faster in SQL than fetching them all into Python and using `len()`).

---

## 12. SQL ↔ SQLModel Reference Table

This table summarizes the mappings between the SQL you learned in Reading 1 and the SQLModel Python equivalents covered in this reading:

| SQL | SQLModel / Python |
|-----|-------------------|
| `SELECT * FROM accounts` | `select(Account)` |
| `SELECT owner, balance FROM accounts` | `select(Account.owner, Account.balance)` |
| `WHERE email = 'x'` | `.where(col(Account.email) == "x")` |
| `WHERE balance > 300` | `.where(col(Account.balance) > 300)` |
| `WHERE owner LIKE 'S%'` | `.where(col(Account.owner).startswith("S"))` |
| `ORDER BY owner ASC` | `.order_by(col(Account.owner))` or `.order_by(col(Account.owner).asc())` |
| `ORDER BY balance DESC` | `.order_by(col(Account.balance).desc())` |
| `LIMIT 1` | `.limit(1)` |
| `SELECT * FROM accounts WHERE id = 1` | `session.get(Account, 1)` |
| `INSERT INTO accounts (...)` | `session.add(Account(...))` then `session.commit()` |
| `UPDATE accounts SET balance = ... WHERE id = 1` | Modify attribute, `session.add(account)`, `session.commit()` |
| `DELETE FROM activity WHERE id = 6` | `session.delete(activity)` then `session.commit()` |
| `SELECT COUNT(*) FROM accounts` | `select(func.count()).select_from(Account)` |
| `SELECT SUM(balance) FROM accounts` | `select(func.sum(Account.balance))` |
| `GROUP BY account_id` | `.group_by(Activity.account_id)` |

---

## Summary

The ORM does not replace SQL — it translates it. Every `select()`, `.where()`, `.order_by()`, and `.limit()` call maps to a SQL clause you already know. The benefit is that you get **type safety**, **Python-native syntax**, and the ability to compose queries **programmatically**.

Key takeaways:

| Concept | Key Takeaway |
|---------|-------------|
| **`select(Model)`** | Builds a `SELECT` statement. Nothing runs until `session.exec()`. |
| **`session.exec()`** | Sends the statement to the database and returns results. |
| **`session.get(Model, pk)`** | Shortcut for primary key lookups, checks the identity map first. |
| **`.where()`** | Filters rows — Python operators (`==`, `>`, `<`) map to SQL operators. |
| **`.order_by()`** | Sorts results. Use `.desc()` for descending order. |
| **`.limit()`** | Restricts the number of returned rows. |
| **`col()`** | Wraps a model attribute for use in query expressions. |
| **`session.add()` + `commit()`** | The ORM equivalent of `INSERT` and `UPDATE`. |
| **`session.delete()` + `commit()`** | The ORM equivalent of `DELETE`. |
| **`func.count()`, `func.sum()`** | SQL aggregate functions accessible from Python. |

---

## Looking Ahead

Reading 2 dives deeper into the **Session** object — what `commit()` actually does, what happens when you forget it, and why each HTTP request should get its own session. Understanding sessions is essential for writing correct, reliable database code in a web application.
