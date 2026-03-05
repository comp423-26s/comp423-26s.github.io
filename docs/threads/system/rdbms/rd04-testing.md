---
code: RD23
title: "Testing with Databases"
threads: ["System / RDBMS"]
authors: [Kris Jordan]
date: 2026-03-05
due: 2026-03-06
---

# Testing with Databases

## Learning Objectives

After completing this reading, you will be able to:

1. Explain why testing against a real database is valuable.
2. Understand the motivation for generating a fresh schema per test.
3. Understand why tests may pass individually but fail in a suite.
4. Distinguish strict unit tests from database-backed integration tests and explain why both matter.
5. Identify anti-patterns: global sessions and shared test state.
6. Choose Assert strategies: return-value checks vs persisted-state verification.

---

## 1. Why Test Against a Real Database?

You might wonder: *"Can't I just **unit** test my services without a database?"*

The answer is that since our services use a database session directly, **testing them against a real database is the most natural and valuable approach**. Consider what a real database catches:

| Bug                                                           | Caught Without DB? | Caught by Real DB? |
| ------------------------------------------------------------- | ------------------ | ------------------ |
| Wrong column name in a `WHERE` clause                         | No                 | **Yes**            |
| Missing `NOT NULL` constraint                                 | No                 | **Yes**            |
| Unique constraint not declared                                | No                 | **Yes**            |
| `commit()` never called                                       | No                 | **Yes**            |
| SQL syntax error in a query                                   | No                 | **Yes**            |
| Business logic error (e.g., transfer allows negative balance) | **Yes**            | **Yes**            |
| Transaction not atomic (partial commit)                       | No                 | **Yes**            |

Testing services against a real PostgreSQL database exercises the full SQLModel and SQLAlchemy stack, from Python objects to generated SQL to actual table storage, using the same database engine you run in development and production. Testing against a different engine, like SQLite's fast in-memory database, can mask SQL dialect differences and constraint behaviors that would only surface in production.

---

## 2. Test Isolation: A Core Concern in Systems Integration Tests

When you run a test suite, each test must start from a **known state**. Since the database is an external system designed to persist our data, by default it persists all commited changes between tests. So if Test A inserts a row and Test B expects an empty table, then running them in sequence will cause Test B to fail. This is the **test isolation** problem.

### Testing Strategy: Fresh Schema per Test

The simplest approach, and the one I recommend for this course, is to create a **fresh schema for each test** by creating and dropping tables on a **dedicated test database** in PostgreSQL:

```python
import pytest
from sqlmodel import SQLModel, Session, create_engine

TEST_DATABASE_URL = "postgresql://postgres:mysecretpassword@db:5432/bank_test"

@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE_URL)

@pytest.fixture
def session(engine):
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)
```

Every test that injects the `session` fixture gets fresh, empty tables. This is what the `SQLModel.metadata.create_all(engine)` call is achieving. After the test, all tables are dropped with the call to `drop_all`, so there is zero possibility of cross-test contamination as long as tests are not being run in parallel.

### What does `scope="session"` mean here?

`@pytest.fixture(scope="session")` means pytest will create the `engine` fixture **once per full test run**, then reuse it across all tests. This is valuable because creating an engine and connection pool is relatively expensive, and there is no need to rebuild it for every test.

At the same time, notice that `session()` has no explicit scope, so it defaults to function scope (one per test). That gives you the best of both worlds:

- Reuse expensive engine setup across the test suite.
- Keep database/session state isolated per individual test.
- Make tests faster without coupling their data.

### Seeding Data

Your most valuable database integration tests will require some data. When the session is injected, tables are empty. The process of adding test data into a database is called _seeding_.

It is perfectly fine to share setup helpers/fixtures for repeated seed data (for example, `_seed_two_accounts` for transfer tests in our lecture example). The key is to share **setup logic**, not mutable database state.

Good practice:

- Keep reusable seed fixtures/helpers close to the tests that use them (often in the same test module).
- Build data fresh for each test using function-scoped fixtures.

Be careful with global prepopulation across the whole suite (for example, one big fixture in `conftest.py` that inserts many rows once): this can become fragile, create hidden test dependencies, and break when test order changes. There is a natural temptation to do this in early stage projects, and it can work quite well for small enough projects, but as the scope of a product grows it becomes quite painful to work with. This was true of the CS XL web site and we are currently undertaking an effort to improve the database integration test suite to avoid a large, fragile seed data set shared across all backend tests. One other issue as the seed dataset grows is that it takes longer for every individual test to seed the data before running a test, which is wasteful because most tests only require data from a few database tables.

---

## 3. Why Tests Can Pass Alone but Fail Together

Now that you have a sense of what the best practice is with isolation, it's worth reflecting and discussing briefly what you might encounter if the isolation is not properly setup.

Without intentional setup and teardown of a database, you can have an experience where you run a single test and have it pass but run the whole suite and it fails. Alternatively, the same test succeeds the first run and fails the second. When this occurs with database tests, these are hints that there is persistent state lingering in the background between test runs. For a healthy test suite, you do not want any shared state between individual tests. Here are the most common sources and fixes:

### Shared State Between Tests

Test A inserts an account with email "spongebob@unc.edu". Test B also tries to insert "spongebob@unc.edu" and hits a unique constraint violation.  If two tests use the same database without proper isolation via resetting tables or transactions, data from one test will be present in the other.

**Fix:** Use the per-test session fixture that drops all tables after each test shown in the previous section.

### Test Order Dependencies

If Test A relies on data created by Test B, and the test runner happens to change the order, Test A fails.

**Fix:** Each test should take ownership of its test data and the test suite should completely reset the database between runs. Do not assume data from another test exists. Where there is redundancy in test data, create helper functions that individual tests call out to.

### Global Session or Engine

If the session is created at module level rather than in a fixture, all tests share the same session:

```python
# BAD: Global session
engine = create_engine("postgresql://postgres:mysecretpassword@db:5432/bank_test")
session = Session(engine)  # Shared across all tests!
```

Changes in one test affect the next. And if one test calls `rollback()`, it undoes another test's changes.

**Fix:** Create primary sessions inside fixtures. We will see one motivation for creating an additional session, inside of a test function, when we get to discussing end-to-end backend tests.

---

## 4. What to Assert: Return Values vs Persisted State

In database integration tests, asserting only a method's return value can be enough **sometimes**, but not always. A good rule is:

- If the method is intended to be a pure read/query method, assert the return value.
- If the method is intended to mutate persistent state, also confirm the persisted effect.

### When return-value assertions are usually sufficient

For read-oriented service methods (for example `list_all_accounts`, `get_by_id`, `search_by_email`), the return value is the contract. If the method returns the expected objects given known seeded data, that is usually the most direct and sufficient assertion.

### When to add persistence assertions

Add persistence assertions when the method performs writes or transaction logic, especially when correctness depends on side effects:

- Create/update/delete operations
- Methods that call `commit()`
- Multi-step transactional logic (for example transfers)
- Any method where a bug could return a "correct-looking" object but fail to persist correctly

In these cases, treat the return value as one assertion and the database state as another assertion.

### Should you use an additional session for verification during the Assert steps?

A SQLAlchemy/SQLModel session has an identity map and local state that _can_ mask persistence bugs. If you verify with the same session used for the write, you may accidentally observe in-memory state rather than true persisted state. To avoid this, for higher-confidence persistence checks, you can open a **new** session and query the database in a separate session. In this course, we do not _require_ this additional level of isolation for verification, but you are encouraged to attempt it. 

## 5. Why Integration Tests Are Necessary

As we have learned, a **unit test** pedantically means the test subject is isolated to a single class/function, with dependencies replaced with doubles. By that definition, tests that hit a real PostgreSQL database are **integration tests** because they involve an external dependency.

You will still hear professionals casually call these kinds of service tests "unit tests" even when they hit a database. For clarity in this course, treat DB-hitting service tests as integration tests and mark them so you can control running these tests, which are much slower than true unit tests due to the integration with data persistence, when needed:

```python
import pytest

@pytest.mark.integration
def test_list_all_accounts(account_svc):
    assert account_svc.list_all() == []
```

This is useful when you want fast feedback from pure unit tests during development. The full database-backed integration tests can be run less frequently, before commits and merging, and in the full continuous integration (CI) pipeline.

Of course, it **is** possible to mock an injected session in the service layer and verify collaboration with the ORM. For example, that a service method calls expected session/query methods. That can be useful for narrow unit-level checks, but for methods that directly communicate with a database, integration tests provide much higher value because they validate actual query behavior and persisted effects.

---

## 6. See Lecture's `orm-demo` for Complete Examples

As we are exploring in lecture, the `orm-demo` project has testing examples, fixtures, and configuration to illustrate these concepts. You can look toward it while you are implementing your persistence layer in the next task.

## Summary

| Principle                    | Practice                                                                 |
| ---------------------------- | ------------------------------------------------------------------------ |
| Test against a real database | Use a test PostgreSQL database (`bank_test`) for service tests           |
| Isolate every test           | Create + drop tables per test via fixtures                               |
| Keep tests independent       | Each test creates its own data                                           |
| Share setup carefully        | Keep reusable seed helpers module-local; avoid suite-global seeded state |
| Assert at the right depth    | Reads: assert returns; Writes: also verify persisted state               |
| Test at the right layer      | Services → real DB; Integration → full HTTP stack                        |
| Control expensive test scope | Mark DB-hitting tests with `@pytest.mark.integration`                    |
| Avoid global state           | Sessions and engines live in fixtures, not module scope                  |
