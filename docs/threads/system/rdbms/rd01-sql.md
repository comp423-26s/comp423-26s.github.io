---
code: RD20
title: "SQL Primer for COMP423"
threads: ["System / RDBMS"]
authors: [Kris Jordan]
date: 2026-02-27
due: 2026-03-02
---

# SQL Primer for COMP423

## Learning Objectives

After completing this reading, you will be able to:

1. Explain the relational model in practical software engineering terms.
2. Differentiate between a primary key and a unique constraint.
3. Describe what an index does and why lookups by column are faster with one.
4. Predict what happens when a uniqueness constraint is violated.
5. Explain what a foreign key constraint enforces (and what happens when it's violated).
6. Write SQL queries for filtering, sorting, updating, and aggregating (including `GROUP BY`).
7. Write a multi-statement SQL transaction with `BEGIN` / `COMMIT` and describe ACID at a high level.

---

## 1. What is a Relational Database?

A **relational database** stores data in **tables**. Each table has **rows** (records) and **columns** (fields). Relational databases are useful because they let us connect related data, enforce rules, and support many users safely at the same time.

Unlike in-memory Python data structures, relational databases **persist data to disk**. That means data remains even after the program or server stops. This makes them essential for long-term, real-world applications like banking, e-commerce, content management systems, and the apps you build in this course.

### A Brief History

The concept of relational databases was introduced by **Edgar F. Codd** in 1970 while working at IBM. He proposed the **relational model**, which organizes data into structured tables and uses mathematical **relational algebra** for querying and manipulating data.

Before relational databases, many systems used **hierarchical** or **network databases**, which were rigid and harder to scale. Codd's model made data easier to organize and query.

**Structured Query Language (SQL)** was developed in the 1970s at IBM as a way to interact with relational databases. It became the standard language for querying and managing relational data and is used by every major database system today.

### Popular Relational Databases

| Database                 | Notes                                                          |
| ------------------------ | -------------------------------------------------------------- |
| **PostgreSQL**           | Open-source, feature-rich, widely used for modern applications |
| **MySQL**                | Common in web applications, especially the LAMP stack          |
| **Microsoft SQL Server** | Enterprise-level, common in .NET environments                  |
| **Oracle Database**      | Widely used in large corporations                              |

In this course, we use **PostgreSQL** both for hands-on SQL practice and as the database for our Python web app. Running PostgreSQL as a separate process is realistic: your app is one process, the database is another, and they communicate over a network connection.

---

## 2. Setting Up PostgreSQL with Docker

To follow along, run PostgreSQL in Docker and keep `psql` open as you read.

### Pull and Run PostgreSQL

From your host machine's terminal:

```sh
docker run \
  --name postgres \
  --env POSTGRES_PASSWORD=secret \
  --publish 5432:5432 \
  --detach \
  postgres:latest
```

| Flag                          | Purpose                                 |
| ----------------------------- | --------------------------------------- |
| `--name postgres`             | Names the container `postgres`          |
| `--env POSTGRES_PASSWORD=...` | Sets the default password               |
| `--publish 5432:5432`         | Maps port 5432 from container to host   |
| `--detach`                    | Runs in the background                  |
| `postgres:latest`             | Uses the latest stable PostgreSQL image |

If `docker run ... --name postgres` fails because the container already exists, try simply running the `start` command as follows:

```sh
docker start postgres
```

### Connect to PostgreSQL

```sh
docker exec \
  --interactive \
  --tty \
  --user postgres \
  postgres \
  psql
```

This runs the `psql` command-line client inside the existing container.

| Flag                              | Purpose                                                                 |
| --------------------------------- | ----------------------------------------------------------------------- |
| `--interactive`, `-i`             | Keep STDIN open so you can interact with the process inside the container |
| `--tty`, `-t`                     | Allocate a pseudo-TTY (enables interactive terminal features)           |
| `--user postgres`                 | Run the command as the specified user inside the container (`postgres`) |
| `<container>` (e.g., `postgres`)  | The name or ID of the container to execute the command in               |
| `psql`                            | The command executed inside the container (PostgreSQL interactive client) |

!!! note "psql prompt & shell"
    After running `psql` you will see a database prompt such as `postgres=#`. This indicates you are in the PostgreSQL interactive SQL shell (a client connected to the server) rather than the Bash shell. Commands entered here are SQL statements which are terminated with a semicolon `;`. To quit the SQL shell, type `\q` or press `Ctrl-D`.

### Where is the Data Stored?

When running Docker without explicit volume mapping, PostgreSQL stores data **inside the container's filesystem**. Stopping and restarting the container preserves the data, but *removing* the container (`docker rm postgres`) deletes everything. 

In production you would mount a *volume*, which is persistent storage managed by Docker that lives outside a container’s writable layer (typically on the host or via a volume driver). Volumes persist across container restarts and removals, can be shared between containers, and are the standard way to store durable data.

### Useful Container Commands

```sh
docker stop postgres     # Stop the container (data preserved)
docker start postgres    # Restart (data still there)
docker rm postgres       # Remove container (data lost!)
```

---

## 3. SQL: A Domain-Specific Language

SQL (**Structured Query Language**) is a language designed for relational databases. Unlike general-purpose languages like Python, SQL is **domain-specific**: it is focused on storing, retrieving, and changing structured data.

You can think of SQL in two big categories:

### DDL (Data Definition Language)

DDL manages the **structure** (schema) of the database.

| Command        | Purpose                         |
| -------------- | ------------------------------- |
| `CREATE TABLE` | Define a new table              |
| `ALTER TABLE`  | Modify an existing table        |
| `DROP TABLE`   | Delete a table and all its data |

### DML (Data Manipulation Language)

DML operates on the **data** stored in tables.

| Command       | Purpose              |
| ------------- | -------------------- |
| `INSERT INTO` | Add new rows         |
| `SELECT`      | Retrieve rows        |
| `UPDATE`      | Modify existing rows |
| `DELETE`      | Remove rows          |

---

## 4. Key Abstractions: Tables, Columns, and Rows

Now that you have access to a database via `psql`, let's try it out!

### Tables

A **table** is the basic structure in an RDBMS. It represents a collection of related data, similar to a spreadsheet, but with more rigid and well defined structure.

Let's create our first table using SQL's **DDL** (`CREATE TABLE`). In your `psql` prompt, run:

```sql
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    owner TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    balance INTEGER NOT NULL DEFAULT 0
);
```

You should see a success message like `CREATE TABLE`.

### Columns (Fields)

A **column** defines one attribute and its allowed data type.

PostgreSQL has many data types you can learn about in the [official documentation](https://www.postgresql.org/docs/current/datatype.html). For a quick overview, here are some of the common PostgreSQL data types:

| Data Type                   | Description                                                |
| --------------------------- | ---------------------------------------------------------- |
| `INTEGER`                   | Whole numbers (e.g., 1, 42, -7)                            |
| `SERIAL`                    | Auto-incrementing integer (commonly used for primary keys) |
| `TEXT`                      | Variable-length string (unlimited size)                    |
| `VARCHAR(n)`                | String with a maximum length of `n` characters             |
| `BOOLEAN`                   | True or False values                                       |
| `DATE`                      | Stores dates (YYYY-MM-DD)                                  |
| `TIMESTAMP`                 | Stores date and time information                           |
| `DECIMAL(p, s)`             | Precise fixed-point decimal numbers                        |
| `REAL` / `DOUBLE PRECISION` | Floating-point numbers                                     |

Columns can also carry **constraints** that enforce rules on the data:

| Constraint | Meaning                                                      |
| ---------- | ------------------------------------------------------------ |
| `NOT NULL` | The column cannot be empty.                                  |
| `UNIQUE`   | All values in the column must be distinct.                   |
| `CHECK`    | Enforces a Boolean condition (e.g., `CHECK (balance >= 0)`). |
| `DEFAULT`  | Assigns a value automatically if none is provided.           |

Some columns have fixed maximum widths. For example, `VARCHAR(255)` prevents values longer than 255 characters.

### Verifying Your Table with SQL

After creating a table, it is good practice to **verify** it exists and that its columns look the way you expect. We will learn more about the structure of these SQL queries soon, for now you can scan them, copy, paste, and run in psql.

In many relational databases, including PostgreSQL, you can query the database to see its tables and information about columns in a table.

To list tables in the current database (restricting to the `public` schema in PostgreSQL):

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

To list columns of the `accounts` table:

```sql
SELECT
    ordinal_position,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
    AND table_name = 'accounts'
ORDER BY ordinal_position;
```

Other RDBMSs organize schemas/catalogs slightly differently, but the general idea is the same: query the database's catalog tables to confirm the schema you just created.

### Rows (Records)

A **row** represents a single entry in a table — one specific combination of values across all the columns.

An analogy to **Object-Oriented Programming** is helpful here:

- A **table** is like a class definition.
- **Columns** define the attributes of the class.
- **Rows** are like instances (objects) created from the class.

Like all analogies, it is not a perfect one, which is why we will learn about mappings from OOP to SQL soon, but these are close conceptual relationships.

Let's insert some data using SQL's **DML** (`INSERT INTO`). Run the following in `psql`:

```sql
INSERT INTO accounts (owner, email, balance) VALUES ('SpongeBob', 'spongebob@unc.edu', 500);
INSERT INTO accounts (owner, email, balance) VALUES ('Squidward', 'squidward@unc.edu', 250);
INSERT INTO accounts (owner, email, balance) VALUES ('Patrick', 'patrick@unc.edu', 1000);
```

Notice we do not supply `id` — the `SERIAL` type auto-generates it for each row.

The table looks like this:

| id  | owner   | email               | balance |
| --- | ------- | ------------------- | ------- |
| 1   | SpongeBob  | spongebob@unc.edu   | 500     |
| 2   | Squidward  | squidward@unc.edu   | 250     |
| 3   | Patrick    | patrick@unc.edu     | 1000    |

Each row is similar to a Python object, with some data type and constraint enforcement differences between Python and SQL:

```python
class Account:
    def __init__(self, id: int, owner: str, email: str, balance: int):
        self.id = id
        self.owner = owner
        self.email = email
        self.balance = balance
```

---

## 5. Primary Keys vs. Unique Constraints

These two concepts are related but serve different purposes.

### Primary Key

A **primary key** uniquely identifies each row in a table. A table should have exactly one primary key. It is:

- **Unique** — no two rows share the same primary key value.
- **Not null** — a primary key column can never be empty.
- **Immutable by convention** — you generally never change a primary key after a row is created.

In our `accounts` table, `id SERIAL PRIMARY KEY` serves this role. The `SERIAL` type auto-increments, so the database assigns `1`, `2`, `3`, ... automatically.

For many applications, `SERIAL` integers are common. At very large scale, teams often use **UUIDs** because they can be generated across different systems without collisions.

### Unique Constraint

A **unique constraint** ensures that no two rows share the same value in a given column, but it is *not* the row's identity. A table can have **many** unique constraints but only **one** primary key.

In our example, `email TEXT UNIQUE NOT NULL` is a unique constraint. It prevents two accounts from sharing the same email address, but the *identity* of each row is still the `id`.

### What Happens When You Violate a Constraint?

Try inserting a duplicate email in your `psql` console:

```sql
INSERT INTO accounts (owner, email, balance)
VALUES ('Eve', 'spongebob@unc.edu', 0);
```

PostgreSQL responds with an error:

```
ERROR:  duplicate key value violates unique constraint "accounts_email_key"
DETAIL:  Key (email)=(spongebob@unc.edu) already exists.
```

The INSERT fails entirely — no partial row is created. This is the database **enforcing data integrity** for you, which is far safer than checking for duplicates in application code.

---

## 6. Indexes — Making Lookups Fast

When you run a query like:

```sql
SELECT * FROM accounts WHERE email = 'squidward@unc.edu';
```

the database needs to find the matching row. Without any special data structure, it must scan *every row* in the table — a **sequential scan**. For 3 rows this is trivial; for 3 million rows it is painfully slow.

An **index** is a separate data structure (often a **B-tree**) that the database maintains alongside the table. It maps column values to row locations, like the index at the back of a textbook maps topics to page numbers.

### When Are Indexes Created Automatically?

- A **primary key** always gets an index automatically.
- A **unique constraint** always gets an index automatically (the database needs it to efficiently enforce uniqueness).

So in our `accounts` table, both `id` and `email` are automatically indexed.

### When Do You Need to Create an Index Manually?

If you frequently filter or sort on a column that is *not* a primary key or unique, you should create an index:

```sql
CREATE INDEX idx_accounts_owner ON accounts (owner);
```

Now `SELECT * FROM accounts WHERE owner = 'SpongeBob';` can use the index instead of scanning every row.

### The Trade-off

Indexes speed up reads but add some write overhead, because the index must be updated on inserts, updates, and deletes. In most applications, the read-speed gain is worth this cost.

---

## 7. Next Steps: The Activity Table

Before we move on to querying, let's establish another table for our banking system. The activity table records every deposit and withdrawal:

```sql
CREATE TABLE activity (
    id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    activity_type TEXT NOT NULL CHECK (activity_type IN ('WD', 'DEP')),
    amount INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

This introduces a **foreign key** constraint: `activity.account_id` must refer to an existing row in `accounts(id)`.

- If you try to insert an activity entry for a nonexistent account, PostgreSQL will reject it.
- By default, PostgreSQL will also prevent you from deleting an account row if activity rows still reference it.

`activity_type` is a simple enumeration: `DEP` for deposit and `WD` for withdrawal.

### Insert Some Activity Entries

```sql
INSERT INTO activity (account_id, activity_type, amount) VALUES (1, 'DEP', 500);
INSERT INTO activity (account_id, activity_type, amount) VALUES (2, 'DEP', 250);
INSERT INTO activity (account_id, activity_type, amount) VALUES (3, 'DEP', 1000);
INSERT INTO activity (account_id, activity_type, amount) VALUES (1, 'WD', 100);
INSERT INTO activity (account_id, activity_type, amount) VALUES (1, 'DEP', 50);
INSERT INTO activity (account_id, activity_type, amount) VALUES (2, 'WD', 30);
```

!!! note "Convention"
    `amount` is stored as a **positive** integer. The `activity_type` indicates whether the activity adds to the balance (`DEP`) or subtracts from it (`WD`).

---

## 8. Querying: SELECT, WHERE, ORDER BY, LIMIT

In this section, you will see several `SELECT` statements. A `SELECT` query asks the database to **return a result table** (a set of rows and columns) based on rules you specify.

### How to Read a Basic `SELECT` Query

Here is the basic shape you will see repeatedly:

```sql
SELECT <columns>
FROM <table>
WHERE <row_filter>
ORDER BY <sort_key>
LIMIT <max_rows>;
```

Not every query uses every clause, but the idea stays the same.

#### The pieces (syntax + meaning)

- `SELECT` … chooses **which columns** to return.
    - `*` is a wildcard meaning "all columns".
    - You can list columns separated by commas, like `owner, balance`.
- `FROM` … names the **table** you are reading from.
- `WHERE` … filters down to only the **rows that match boolean conditions (predicates)**.
    - Example operators you will see:
        - `=` equality (exact match)
        - `>` greater than
        - `LIKE` pattern matching (described below)
- `ORDER BY` … sorts the returned rows.
    - `ASC` means ascending (smallest → largest, A → Z).
    - `DESC` means descending (largest → smallest, Z → A).
    - Without `ORDER BY`, the database is free to return rows in any order.
- `LIMIT` ... restricts how many rows are returned.
- `;` ends the statement in `psql`, like a statement in C-family programming languages

#### A note on literals

- String values use **single quotes**, like `'spongebob@unc.edu'`.
- `LIKE 'B%'` means "starts with B" because `%` is a wildcard meaning "any sequence of characters".

#### A note on evaluation order (mental model)

When reading a `SELECT` query, it often helps to think:

1. `FROM` (pick the table)
2. `WHERE` (filter rows)
3. `SELECT` (choose columns)
4. `ORDER BY` (sort)
5. `LIMIT` (take the first N)

This is not a full description of how the database executes queries internally, but it is a useful way to understand what the clauses mean.

Now let's interactively explore this syntax with examples that build up to more complex select statements. Follow along with each of the examples below:

### Retrieve All Rows

```sql
SELECT * FROM accounts;
```

| id  | owner   | email               | balance |
| --- | ------- | ------------------- | ------- |
| 1   | SpongeBob  | spongebob@unc.edu   | 500     |
| 2   | Squidward  | squidward@unc.edu   | 250     |
| 3   | Patrick    | patrick@unc.edu     | 1000    |

### Select Specific Columns

```sql
SELECT owner, balance FROM accounts;
```

### Filter with WHERE

Find a specific account by email:

```sql
SELECT * FROM accounts WHERE email = 'spongebob@unc.edu';
```

Find accounts with a balance above 300:

```sql
SELECT * FROM accounts WHERE balance > 300;
```

Find accounts whose owner name starts with "S":

```sql
SELECT * FROM accounts WHERE owner LIKE 'S%';
```

### Sorting with ORDER BY

Sort by balance, with the highest balances first:

```sql
SELECT * FROM accounts ORDER BY balance DESC;
```

Sort alphabetically by owner name:

```sql
SELECT * FROM accounts ORDER BY owner ASC;
```

### Limiting Results

Get the single largest account:

```sql
SELECT * FROM accounts ORDER BY balance DESC LIMIT 1;
```

---

## 9. Updating Data

The `UPDATE` statement modifies existing rows. In a banking system, updates are the bread and butter — every deposit and withdrawal changes a balance.

### How to Read an `UPDATE` Statement

Here is the common shape:

```sql
UPDATE <table>
SET <column> = <expression>
WHERE <row_filter>;
```

- `UPDATE <table>` chooses which table you want to change.
- `SET` describes **what to change**. The right-hand side can be an expression.
    - `balance = balance + 100` means "take the old `balance` value and add 100".
    - You can update multiple columns by separating assignments with commas.
- `WHERE` chooses **which rows** to modify.
    - `WHERE id = 1` targets the row whose primary key is 1.
    - If no rows match, then nothing is updated.

!!! warning "Always double-check `WHERE`"
    If you omit the `WHERE` clause, the update applies to **every row** in the table.

### Deposit $100 into SpongeBob's Account

```sql
UPDATE accounts SET balance = balance + 100 WHERE id = 1;
```

After this, SpongeBob's balance is `600`.

### Withdraw $50 from Squidward's Account

```sql
UPDATE accounts SET balance = balance - 50 WHERE id = 2;
```

Squidward's balance is now `200`.

!!! warning "Always Use a WHERE Clause!"

    Running `UPDATE accounts SET balance = 0;` *without* a `WHERE` clause would set **every** account's balance to zero. Always double-check your `WHERE` before executing an `UPDATE`.

### Recording Activity + Updating Balances as One Atomic Transaction

In a real system, you rarely want to update a balance without also recording *why* it changed. We can group multiple statements into a **single transaction** so they succeed or fail together.

Here is a simple example: transfer $200 from SpongeBob (account 1) to Squidward (account 2). This updates balances and inserts matching activity entries.

```sql
BEGIN;

-- Record the intent (activity log)
INSERT INTO activity (account_id, activity_type, amount) VALUES (1, 'WD', 200);
INSERT INTO activity (account_id, activity_type, amount) VALUES (2, 'DEP', 200);

-- Apply the balance changes
UPDATE accounts SET balance = balance - 200 WHERE id = 1;
UPDATE accounts SET balance = balance + 200 WHERE id = 2;

COMMIT;
```

If any statement in the transaction fails (for example, the foreign key constraint on `activity.account_id` or a check constraint), the whole transaction is rolled back and **none** of the changes take effect.

### ACID: The Four Guarantees of a Transaction

The properties that make transactions trustworthy are summarized by **ACID**.

| Property | One-Sentence Definition | Banking Example |
|----------|------------------------|----------------|
| **Atomicity** | All operations in a transaction succeed together, or none of them take effect. | A transfer debits SpongeBob *and* credits Squidward, or neither balance changes. |
| **Consistency** | A transaction moves the database from one valid state to another — no constraint is violated. | An activity insert with a nonexistent `account_id` is rejected because of the foreign key. |
| **Isolation** | Concurrent transactions do not see each other's uncommitted work. | While Request A is transferring money, Request B reading balances sees the *old* values until A commits. |
| **Durability** | Once a transaction commits, the data is permanently saved — it survives crashes, power failures, and restarts. | After `COMMIT;` returns, the new balances and activity rows persist even if the server crashes one millisecond later. |

!!! note "Isolation levels"
    In practice, databases offer different **isolation levels** (Read Committed, Repeatable Read, Serializable) that trade strictness for performance. PostgreSQL defaults to **Read Committed**. We won't dive into isolation levels in this course, but you should know the concept exists.

---

## 10. Aggregating Data

SQL provides **aggregate functions** that compute one result from many rows.

### How to Read Aggregate Queries

Aggregates like `COUNT(*)` and `SUM(amount)` combine many rows into a single value.

For example:

```sql
SELECT COUNT(*) FROM accounts;
```

means "count how many rows are in `accounts`".

#### Aliases with `AS`

You will often see `AS name` to give a computed column a readable name:

- `... AS net_activity` means "label this computed column as `net_activity`" in the results.

#### Conditional logic with `CASE`

Sometimes you need conditional logic inside an expression. SQL uses a `CASE` expression:

```sql
CASE WHEN <condition> THEN <value_if_true> ELSE <value_if_false> END
```

In our banking example, we store `amount` as a positive integer and use `activity_type` to decide whether to add or subtract it.

| Function      | Purpose                         |
| ------------- | ------------------------------- |
| `COUNT(*)`    | Number of rows                  |
| `SUM(column)` | Total of all values in a column |
| `AVG(column)` | Average value                   |
| `MIN(column)` | Smallest value                  |
| `MAX(column)` | Largest value                   |

### How Many Accounts Exist?

```sql
SELECT COUNT(*) FROM accounts;
```

Result: `3`

### What is the Total Balance Across All Accounts?

```sql
SELECT SUM(balance) FROM accounts;
```

### What is the Net Activity for Each Account in the Activity Table?

If you want an aggregate **per group** (per account), you use `GROUP BY`.

#### `GROUP BY` in One Sentence

`GROUP BY account_id` means: "Partition the rows into one bucket per `account_id`, then compute the aggregates once per bucket."

Here's the pattern:

```sql
SELECT <group_columns>, <aggregate_expressions>
FROM <table>
GROUP BY <group_columns>;
```

Now let's compute the signed net activity and number of entries per account:

```sql
SELECT
    account_id,
    SUM(CASE WHEN activity_type = 'DEP' THEN amount ELSE -amount END) AS net_activity,
    COUNT(*) AS num_entries
FROM activity
GROUP BY account_id
ORDER BY account_id;
```

Read this as: "Group activity rows by `account_id`. For each account, compute the signed net total (deposits add, withdrawals subtract) and count how many activity rows exist."

#### Filtering Rows vs Filtering Groups

- `WHERE ...` filters **rows before** grouping.
- `GROUP BY ...` forms groups.
- Aggregate functions like `SUM(...)` and `COUNT(*)` compute results **per group**.

Sometimes you want to filter based on an aggregate result (for example, "only show accounts whose net activity is positive"). That requires the `HAVING` clause, which is beyond the scope of this reading.

- PostgreSQL docs for `HAVING`: <https://www.postgresql.org/docs/current/sql-select.html#SQL-HAVING>

## 11. Deleting Data

### How to Read `DELETE` Statements

```sql
DELETE FROM <table> WHERE <row_filter>;
```

- `DELETE` removes **rows**.
- The table still exists afterward.
- If you omit the `WHERE` clause, it deletes **all rows**.

To remove rows from a table, use `DELETE`:

```sql
DELETE FROM activity WHERE id = 6;
```

!!! info "A safe DELETE habit"
    Before running a `DELETE ... WHERE ...`, run a `SELECT ... WHERE ...` first to confirm you are targeting the rows you intend.


To delete *all* rows (but keep the table structure):

```sql
DELETE FROM activity;
```

To remove a table in its entirety:

```sql
DROP TABLE <table>;
```

- `DROP TABLE` deletes the **table itself** (its schema and all of its data).
- After dropping a table, you cannot query or insert into it until it is recreated.

```sql
DROP TABLE activity;
```

!!! warning
    `DELETE` and `DROP TABLE` are generally irreversible. Use them carefully, especially without a `WHERE` clause.

---

## Conclusion

In this reading, you practiced the foundations of relational databases and SQL through a simple banking system:

- **Tables, columns, rows** — the building blocks of the relational model.
- **Primary keys** identify rows; **unique constraints** prevent duplicates on other columns.
- **Indexes** make queries fast — they are created automatically for primary keys and unique constraints.
- **DDL** (`CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`) defines structure; **DML** (`INSERT`, `SELECT`, `UPDATE`, `DELETE`) manipulates data.
- **Filtering** (`WHERE`), **sorting** (`ORDER BY`), **limiting** (`LIMIT`), and **aggregating** (`COUNT`, `SUM`, `AVG`) with `GROUP BY` are the workhorses of SQL queries.

In the next reading, you will see how to express these same SQL queries in Python using **SQLModel** — the ORM library that bridges your Python application code and the database.
