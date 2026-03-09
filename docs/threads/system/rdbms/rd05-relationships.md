---
code: RD24
title: "Introduction to Entity Relationships in an ORM"
threads: ["System / RDBMS"]
authors: [Kris Jordan]
date: 2026-03-09
due: 2026-03-10
---

# Relationships: Defining, Querying and Mutating


## Learning Objectives

After completing this reading, you will be able to:

1. Explain what a **foreign key** is and why it matters.
2. Describe **one-to-many** relationships conceptually and in SQLModel.
3. Explain how ORMs represent relationships with `Relationship()`.
4. Work with related entities from either side of a relationship in Python.
5. Recognize how relationship traversal can trigger the **N+1 queries** problem.
6. Write basic **relationship queries** using joins and filters.
7. Explain how SQLModel / SQLAlchemy handle inserts across related entities.
8. Describe how **many-to-many** relationships use join tables.
9. Explain the basics of **delete** and **delete-orphan** cascade behavior.
10. Identify when **normalization** is necessary.

---

## 1. Beyond a Single Table

Throughout this unit, we have worked with two tables: `accounts` and `activity`. In the demo project, the `activity` table records every deposit and withdrawal. Each activity entry references an account via `account_id` which is a column whose value must correspond to an existing account's `id`. The database enforces this relationship through a **foreign key**.

## 2. Foreign Keys

A **foreign key** is a column (or set of columns) in one table that references the **primary key** of another table. It creates a formal link between the two tables and enables the database to enforce **referential integrity**, which is the rule that you cannot reference a row that does not exist.

### Syntax

```sql
CREATE TABLE activity (
    id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    activity_type TEXT NOT NULL CHECK (activity_type IN ('WD', 'DEP')),
    amount INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

The `REFERENCES accounts(id)` clause tells the database:

- Every value in `activity.account_id` **must** correspond to an existing `id` in the `accounts` table.
- Attempting to insert an activity entry for a nonexistent account will fail with an error.
- Attempting to delete an account that still has activity entries will also fail (by default).

### What Happens on Violation?

```sql
INSERT INTO activity (account_id, activity_type, amount)
VALUES (999, 'DEP', 100);
-- ERROR: insert or update on table "activity" violates
--        foreign key constraint "activity_account_id_fkey"
-- DETAIL: Key (account_id)=(999) is not present in table "accounts".
```

The database stops you from creating orphaned records. This is referential integrity in action.

## 3. One-to-Many Relationships

The relationship between `accounts` and `activity` is **one-to-many**: one account can have many activity entries, but each activity entry belongs to exactly one account.

```
accounts                         activity
┌────┬───────────┐              ┌────┬────────────┬──────┬────────┐
│ id │ owner     │              │ id │ account_id │ type │ amount │
├────┼───────────┤        ┌────►├────┼────────────┼──────┼────────┤
│  1 │ SpongeBob │◄───────┤     │  1 │     1      │ DEP  │  500   │
│  2 │ Squidward │◄──┐    │     │  2 │     1      │ WD   │  100   │
│  3 │ Patrick   │   │    └────►│  3 │     1      │ DEP  │   50   │
└────┴───────────┘   │          │  4 │     2      │ DEP  │  250   │
                     └─────────►│  5 │     2      │ WD   │   30   │
                                └────┴────────────┴──────┴────────┘
```

One-to-many is the most common relationship type in application databases. Other types include:

| Relationship     | Example                                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------------------- |
| **One-to-many**  | An account has many activity entries.                                                                   |
| **One-to-one**   | A user's settings in an app.                                                        |
| **Many-to-many** | Students enroll in multiple courses; courses have multiple students. (Implemented with a *join table*.) |

---

## 4. How ORMs Represent Relationships

In our demo project, the `Account` and `Activity` entities declare their relationship using SQLModel's `Relationship()`:

```python title="entities/account.py"
from sqlmodel import Column, Field, Relationship, SQLModel, String

class Account(SQLModel, table=True):
    __tablename__ = "accounts"

    id: int | None = Field(default=None, primary_key=True)
    owner: str
    email: str = Field(sa_column=Column(String, unique=True, nullable=False))
    balance: int = Field(default=0)
    activities: list["Activity"] = Relationship(back_populates="account")
```

```python title="entities/activity.py"
from datetime import datetime
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func
from .activity_type import ActivityType

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
    account: "Account" = Relationship(back_populates="activities")
```

With this setup:

- `account.activities` evaluates to the activity entries for an account — no manual SQL join needed.
- `activity.account` evaluates to the account an activity entry belongs to.

The ORM handles the joins behind the scenes.

### Key Details

- **`foreign_key="accounts.id"`** on `Activity.account_id` tells SQLModel to generate the `REFERENCES accounts(id)` constraint.
- **`Relationship(back_populates="account")`** on `Account.activities` links the two sides of the relationship so changes on one side are reflected on the other.
- **`ActivityType`** is a Python `enum`. SQLModel stores it as a string in the database and converts it automatically.
- **`server_default=func.now()`** translates to a SQL function in the database that sets the `created_at` timestamp automatically upon row insertion, which is why we need `refresh()` after a commit to see the value.

### Working With Related Objects in Python

Before worrying about loading strategies, it helps to see what these relationships feel like when you already have ORM objects in memory.

Suppose you load an account by primary key:

```python
account = session.get(Account, 1)

print(account.owner)
for activity in account.activities:
    print(activity.activity_type, activity.amount)
```

This reads naturally in Python: start from the `Account`, then traverse to its `activities`.

You can also go the other direction:

```python
activity = session.get(Activity, 1)

print(activity.amount)
print(activity.account.owner)
```

Here you start from one `Activity`, then traverse back to the `Account` it belongs to.

This is the main developer experience (DX) benefit of ORM relationships: once objects are loaded, your code can follow connections through object attributes instead of manually reconstructing every relationship with SQL.

### What `back_populates` Actually Does

The `back_populates` setting connects the two relationship attributes so they stay synchronized in Python object state.

If you append a new activity to an account's collection:

```python
account = session.get(Account, 1)
deposit = Activity(activity_type=ActivityType.DEP, amount=200)

account.activities.append(deposit)

assert deposit.account is account
```

And if you assign from the child side:

```python
deposit = Activity(activity_type=ActivityType.DEP, amount=200)
deposit.account = account

assert deposit in account.activities
```

That synchronization is happening in Python memory because the two attributes are paired with `back_populates`.

Two important boundaries to keep in mind:

- `back_populates` keeps the object graph consistent in Python.
- It does **not** persist anything to the database until the session flushes or commits.

If you want more detail beyond this course's level, the official SQLAlchemy relationship basics are here:

- [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)
- [One To Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-many)
- [Many To One](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-one)

### Lazy vs. Eager Loading

The convenient Python navigation above is exactly why loading behavior matters: relationship access looks simple, but it may trigger more database work than you expect.

By default, SQLAlchemy uses **lazy loading**: it does not fetch related objects until you access the attribute. This means `account.activities` triggers a separate SQL query the first time you access it. For small applications this is fine. For high-performance applications, you can use **eager loading** to fetch related data in a single query, but this is beyond our scope in COMP423.

### The N+1 Queries Problem

This lazy-loading behavior leads to one of the most important ORM performance problems: the **N+1 queries problem**.

Suppose you first query for a list of accounts:

```python
accounts = session.exec(select(Account)).all()
```

That is **1 query**.

Then suppose you loop over those accounts and access each account's related activities:

```python
for account in accounts:
    print(account.owner, len(account.activities))
```

That `account.activities` access may look like ordinary Python attribute access, but with lazy loading it can trigger **another SQL query per account**. If there are `N` accounts, the total becomes:

- `1` query to load the accounts
- `N` more queries to load each account's activities

So if `N = 500`, you may accidentally execute **501 queries**.

This is what makes ORM relationship traversal tricky: it *looks* like ordinary object graph traversal in memory, but it may actually be network round-trips to the database over and over again.

### How to Think About the Cost

At the Python level, `account.activities` looks cheap.

At the ORM level, SQLAlchemy checks whether that relationship has already been loaded into the session cache.

At the session cache level, if it has not been loaded, SQLAlchemy generates a new SQL query, sends it to PostgreSQL, waits for the result, constructs Python objects, and then returns the list.

That hidden jump across abstraction levels is the core danger. In normal in-memory OOP, traversing `obj.children` is usually just pointer dereferencing. In an ORM, the same-looking code may cross process boundaries and hit the database repeatedly.

You do not need to become a performance expert yet, but you should develop a **healthy suspicion whenever you traverse relationships of entities of an ORM**.

### Rules of Thumb

- Be suspicious of relationship access inside loops.
- If you load many parent objects, then touch a related field on each one, ask yourself: "Am I doing one query per row?"
- Remember that serialization, templates, debug printing, and response-model construction can also trigger relationship access.
- When you know you will need related data for many rows, that is a sign to consider eager loading strategies such as `selectinload()` or `joinedload()` later on.
- If performance seems surprisingly bad, turn on SQL logging and count the actual queries.

For this course, the key lesson is not to master every loading strategy. It is to avoid the dangerous assumption that relationship traversal is free.

If you want the full SQLAlchemy treatment, the official loading guide is here:

- [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)
- [Lazy Loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#lazy-loading)
- [Preventing unwanted lazy loads using `raiseload`](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#preventing-unwanted-lazy-loads-using-raiseload)

### Writing Custom Queries Across Relationships

Relationship fields are convenient for navigation, but they are not a replacement for writing explicit queries.

Suppose you want all accounts that have at least one deposit activity of at least $750. This is a query concern, so you should express it as a query:

```python
from sqlmodel import select

stmt = (
    select(Account)
    .join(Account.activities)
    .where(
        (Activity.activity_type == ActivityType.DEP) &
        (Activity.amount >= 750)
    )
)

accounts = session.exec(stmt).all()
```

That `join(Account.activities)` call tells SQLAlchemy to join `accounts` to `activity` using the relationship definition you already declared above.

This is useful because the relationship metadata helps SQLAlchemy infer the join condition for you. You do not have to manually restate `activity.account_id = accounts.id` every time.

Another example: suppose you want all activity entries for accounts owned by accounts with the `owner` name `"SpongeBob"`:

```python
stmt = (
    select(Activity)
    .join(Activity.account)
    .where(Account.owner == "SpongeBob")
)

activities = session.exec(stmt).all()
```

This is an important distinction:

- `account.activities` is object navigation on an already-loaded object.
- `select(...).join(...)` is how you shape a database query.

Those are related ideas, but they are not the same operation.

### One Important Caution About Joins

When you join from a parent table to a one-to-many child table, the parent row can appear multiple times in the SQL result set, once for each matching child row.

So if an account has three activity entries, a join-based query may produce three rows involving that same account. That means join queries are powerful, but you should think carefully about whether you want:

- parent objects,
- child objects, or
- a deduplicated parent result.

In other words: explicit joins are often the right way to **filter** or **order** by related data, but they change the query you are asking the database to run.

If you wanted each matching account only once, a common pattern is:

```python
stmt = (
    select(Account)
    .join(Account.activities)
    .where(
        (Activity.activity_type == ActivityType.DEP) &
        (Activity.amount >= 750)
    )
    .distinct()
)
```

If you want more detail on query construction beyond the introductory level here, the official references are:

- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
- [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)

### Where To Read Next on Eager Loading

If you want the next step after this reading, the SQLAlchemy documentation section to bookmark is:

- [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)
- [Select IN loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#select-in-loading)
- [Joined Eager Loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#joined-eager-loading)

For collection relationships like `Account.activities`, `selectinload()` is usually the best first eager-loading strategy to learn.

```python
from sqlalchemy.orm import selectinload
from sqlmodel import select

stmt = select(Account).options(selectinload(Account.activities))
accounts = session.exec(stmt).all()
```

That still performs multiple SQL statements, but importantly it does **not** perform one query per account. Instead, SQLAlchemy loads the accounts first, then loads the related activities for all of those accounts in a batched follow-up query.

Notice here we have an example of what is called a _leaky abstraction_. As much as an ORM tries to abstract away database concerns, since there are some fundamental mismatches in semantic models between these two systems sometimes it is unavoidable that we need to contort high-level code to address lower-level concerns.

Again, this kind of optimization is a little beyond our scope in COMP423, but you should be aware there are techniques for addressing it and look toward official documentation when you work with larger databases and ORMs in future opportunities:

- [What Kind of Loading to Use?](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#what-kind-of-loading-to-use)

### Inserting New Related Records

Relationships are not only for reading. ORMs also help when you create related objects.

Suppose you want to create a new account and its first activity entry in the same unit of work:

```python
new_account = Account(owner="Sandy", email="sandy@example.org", balance=0)
first_deposit = Activity(activity_type=ActivityType.DEP, amount=100)

new_account.activities.append(first_deposit)

session.add(new_account)
session.commit()
session.refresh(new_account)
session.refresh(first_deposit)
```

In SQLModel / SQLAlchemy, you generally **do not manually assign the IDs yourself**. Instead:

- You connect the objects in Python using the relationship.
- The ORM's **unit of work** tracks those objects.
- On flush / commit, it inserts rows in an order that satisfies foreign key constraints.
- It fills in the foreign key values, such as `first_deposit.account_id`, for you.

You could also set the relationship from the other side:

```python
first_deposit.account = new_account
```

That is conceptually equivalent because the two relationship fields are linked by `back_populates`.

### Do You Need `refresh()`?

Usually, you do **not** manually manage the parent's new primary key value and then copy it into the child. SQLAlchemy generally populates database-generated primary keys after a flush / commit.

However, `refresh()` is still important when you want to guarantee that your Python object reflects the database's final stored values, especially for columns populated by the database itself. In our example, `created_at` uses `server_default=func.now()`, so `refresh()` is how we pull that generated timestamp back into the Python object.

So the practical rules of thumb are:

- Let the ORM handle foreign key assignment through the relationship.
- Use `commit()` to persist the work.
- Use `refresh()` when you need database-generated values back on your Python objects.

### What If One Side Already Exists?

This is also common. Suppose the account already exists and you want to add a new activity entry:

```python
account = session.get(Account, 1)
deposit = Activity(activity_type=ActivityType.DEP, amount=50)

account.activities.append(deposit)
session.commit()
session.refresh(deposit)
```

Again, you usually do not need to manually assign `deposit.account_id = account.id`. Appending to the relationship collection gives the ORM enough information to connect the rows correctly.

More broadly, this is a general ORM idea, not just a SQLModel idea: many ORMs try to let you work in terms of object references while the framework handles foreign keys and insert ordering underneath. That convenience is powerful, but it is also why you must remember there is still real SQL and real database work happening underneath the abstraction.

### Many-to-Many Relationships and Join Tables

Some relationships are not one-to-many. A student can enroll in many courses, and each course can have many students. That is a **many-to-many** relationship.

In relational databases, many-to-many relationships are typically implemented with a **join table** that stores one row per pairing:

```sql
CREATE TABLE enrollment (
    student_id INTEGER REFERENCES student(id),
    course_id INTEGER REFERENCES course(id),
    PRIMARY KEY (student_id, course_id)
);
```

In SQLModel, a common pattern is to define that join table as a link model:

```python
class EnrollmentLink(SQLModel, table=True):
    student_id: int | None = Field(
        default=None, foreign_key="student.id", primary_key=True
    )
    course_id: int | None = Field(
        default=None, foreign_key="course.id", primary_key=True
    )


class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    courses: list["Course"] = Relationship(
        back_populates="students", link_model=EnrollmentLink
    )


class Course(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str

    students: list["Student"] = Relationship(
        back_populates="courses", link_model=EnrollmentLink
    )
```

With that setup, the ORM knows how to connect `Student` rows to `Course` rows through the join table.

In the simple case, you can often work with the relationship directly:

```python
student.courses.append(course)
session.commit()
```

The ORM will insert the row in the join table for you.

### Why Join Tables Matter

At first, a join table may look like pure plumbing. But often the relationship itself has data worth storing.

For example, an enrollment is not just "student X is in course Y." You may also care about:

- when the student enrolled,
- what role they have,
- what grade they earned, or
- whether they are on a waitlist.

Once that happens, the join table becomes more than a hidden connector. It becomes a first-class concept in your domain.

In that case, it is often better to model the join table as its own entity, such as `Enrollment`, and give it its own fields and relationships to `Student` and `Course`.

That is one of the deep reasons relational modeling matters: sometimes the most important thing to model is not just the entities, but the relationship between them.

If you want the full SQLAlchemy background, the official references are:

- [Many To Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many)
- [Deleting Rows from the Many to Many Table](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#deleting-rows-from-the-many-to-many-table)
- [Association Object](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object)

---

## 5. Deleting and Cascading

Reading and inserting related data are only part of the story. Deletion is where ORMs often surprise people.

Suppose you delete a parent object:

```python
account = session.get(Account, 1)
session.delete(account)
session.commit()
```

What happens to the related `Activity` rows depends on how the relationship and database constraints are configured.

### Default Behavior vs. Cascade Behavior

Without delete cascade configured, SQLAlchemy will often try to **de-associate** child rows rather than delete them. In a one-to-many relationship, that usually means trying to set the child's foreign key to `NULL`.

But in our banking example, `activity.account_id` is not nullable. That means a parent delete will usually fail unless you explicitly configure a delete strategy that makes sense.

This is a good thing. It forces you to decide what deletion should mean in your domain.

### `delete` and `delete-orphan`

Two important cascade settings to know about are:

- **`delete`**: when the parent is deleted, the related child rows should also be deleted.
- **`delete-orphan`**: if a child is removed from the parent's collection and no longer belongs to that parent, it should be deleted.

For example, a relationship might be configured like this in SQLAlchemy terms:

```python
activities: list["Activity"] = Relationship(
    back_populates="account",
    sa_relationship_kwargs={"cascade": "all, delete-orphan"},
)
```

With that kind of configuration, removing an activity from `account.activities` means more than "stop pointing to it." It can mean "delete this row entirely when the session flushes."

That is powerful, but it should match the domain. If `Activity` rows are part of a permanent transaction ledger, automatic orphan deletion may be the wrong behavior.

### Subtleties of In-Memory State

One common surprise: after you delete an object and flush, Python collections are not necessarily rewritten immediately in memory.

So an object you just deleted may still appear in a relationship collection until the session is committed or expired and the collection is reloaded.

That is one reason delete behavior can feel confusing at first. There is both:

- the database row state, and
- the current in-memory object graph state.

They eventually line up again, but not always at the exact moment a flush occurs.

### General Rule of Thumb

- Be explicit about what deleting a parent should mean for its children.
- Use `delete-orphan` when the child should not exist without that parent.
- Be cautious with delete cascade on many-to-many relationships because it can delete more than you intended.
- Use database constraints and domain rules, not assumptions about "what the ORM probably does."

If you want the authoritative SQLAlchemy references, these are the right places to read:

- [Cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html)
- [delete](https://docs.sqlalchemy.org/en/20/orm/cascades.html#delete)
- [delete-orphan](https://docs.sqlalchemy.org/en/20/orm/cascades.html#delete-orphan)
- [Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#passive-deletes)
- [Notes on Delete](https://docs.sqlalchemy.org/en/20/orm/cascades.html#notes-on-delete-deleting-objects-referenced-from-collections-and-scalar-relationships)

---

## 6. Normalization: When and Why

**Normalization** is the process of organizing database tables to reduce redundancy and improve data integrity. The key idea: *store each piece of information in exactly one place.*

### An Example of Denormalized Data

Imagine storing the account owner's name directly in each activity entry:

```
activity
┌────┬──────────┬──────┬────────┐
│ id │ owner    │ type │ amount │
├────┼──────────┼──────┼────────┤
│  1 │ SpongeBob│ DEP  │  500   │
│  2 │ SpongeBob│ WD   │  100   │
│  3 │ SpongeBob│ DEP  │   50   │
│  4 │ Squidward│ DEP  │  250   │
└────┴──────────┴──────┴────────┘
```

What happens if SpongeBob changes his name? You would need to update **every row** in the activity table that mentions "SpongeBob." If you miss one, your data is inconsistent.

### The Normalized Version

With normalization, as the database is designed in our demo repository, SpongeBob's name is stored **once** in the `accounts` table. Activity entries reference him by `account_id`. Changing his name requires updating a single row:

```sql
UPDATE accounts SET owner = 'SpongeBob SquarePants' WHERE id = 1;
```

All activity queries that join on `account_id` will automatically reflect the new name. This is cleaner, safer, and more efficient.

### When Is Denormalization Acceptable?

Sometimes you intentionally denormalize for performance (e.g., caching a frequently-accessed computed value). The rule of thumb: **start normalized** and denormalize only when profiling shows a measurable performance need.

## Important Concepts Summary

| Concept                      | Key Takeaway                                                                           |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| **Foreign key**              | A column that references another table's primary key, enforcing referential integrity. |
| **One-to-many**              | One row in table A relates to many rows in table B (most common relationship).         |
| **ORM relationships**        | `Relationship()` fields let you navigate between related objects in Python.            |
| **`back_populates`**         | Keeps both sides of a relationship synchronized in Python object state.                |
| **N+1 queries**              | Relationship traversal can silently turn one query into many and seriously hurt performance. |
| **Relationship queries**     | Use explicit `join()` queries when filtering or ordering by related table data.        |
| **Related inserts**          | SQLModel / SQLAlchemy usually handle foreign key assignment and insert ordering for related objects. |
| **Many-to-many**             | Join tables connect rows on both sides and can also store extra data about the relationship. |
| **Delete and cascade**       | Parent deletion and child removal depend on cascade rules, nullability, and domain intent. |
| **Normalization**            | Store each fact once; use foreign keys to connect tables.                              |
