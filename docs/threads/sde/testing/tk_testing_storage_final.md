---
code: TK05
title: Unit and Integration Testing Exercise
date: 2026-02-02
due: 2026-02-06
type: reading
threads: ["Course", "SDE / Testing"]
authors: [Kris Jordan]
---

# Unit and Integration Testing Exercise

This assignment is focused on implementing the storage layer for a URL shortener. You will be completing the implementation of and fully unit and integration testing two classes: `JSONFileIO` (low-level JSON file persistence) and `LinkStore` (logic for storing links).

In future weeks, we will implement the FastAPI routes and service layers. They are not our concern right now. Our goal is to ensure data can be saved to and retrieved from a JSON file reliably.

## Learning Objectives

After successfully completing this exercise, you should be able to:

* Read and navigate a new codebase, understanding its structure and developer tooling.
* Explain the value of test-driven development (TDD) and apply the Red → Green → Refactor cycle.
* Write unit tests that verify individual components in isolation.
* Use mocks to isolate the subject under test from its composed dependencies.
* Use patches to intercept built-in library calls and test logic without side effects.
* Write integration tests that verify components work together with real dependencies.

These skills are foundational to the upcoming quiz and will be assessed in the context of your work on this task.

## Test-driven Development (TDD)

**Test-driven development (TDD)** is a workflow where you write a small, automated unit test *before* you write the code that makes it pass. The goal is to build software in tiny, verifiable steps, using tests as a feedback loop and a safety net.

In this project, you will practice the **Red → Green → Refactor** cycle:

* **Red:** Write a test that describes the behavior you want. Run it and watch it fail (because the feature does not exist yet).
* **Green:** Write the simplest code that makes the test pass. Run the tests until they are all green.
* **Refactor:** Improve the design and readability of your code *without changing behavior*. Re-run tests to confirm you did not break anything.
* **Repeat:** Go back to Red and focus on your next behavior to test and implement.

Done well, TDD helps ensure your tests prove real functionality and gives you a clear "definition of done." It keeps you focused on small, incremental behaviors—preventing you from becoming overwhelmed or trying to implement too much at once. It also encourages you to think critically about your interface design. If your interface feels clunky while writing a test, that's a signal to reconsider your design choices. (Note: In this project, we are providing a sensible enough design that's suitable for testing. When the time comes for you to design your own interfaces, classes, and methods, this is worth remembering, though!)

## Project Setup

This project begins from a new repository, setup very similar to where yours left off in TK04.

You can begin the task by accepting the following GitHub Classroom assignment: https://classroom.github.com/a/ItT31Yka

From a terminal, in whatever directory on your _host machine_ you keep your coursework projects, you should clone your repository. Open that directory as a workspace in VSCode and then reopen the workspace in a dev container.

## 1. Guided Code Read

Before writing any code, you should review the existing repository to understand the context. Read these files in the following order:

1.  **README.md**  
    Overview of the project, technical stack (Python 3.14, FastAPI), and developer tooling commands (`uv`, `pytest`, etc.).

2.  **scripts/run-qa.sh**  
    The master script that runs all checks (linting, formatting, type checking, tests). Open and read the commands of this `bash` script to understand what it does. Run this frequently and _always_ before merging back into main! Go ahead and try running this script to be sure your dev container installed properly by running this command in the built-in terminal: `./scripts/run-qa.sh`

3.  **src/models/link.py**  
    Defines the `Link` data model using Pydantic. Note the fields `slug` and `target`.

4.  **src/store/json_file_io.py**  
    A low-level wrapper around Python's `json` module. Note that `load()` is implemented, but `persist()` is just a stub.

5.  **src/store/link_store.py**  
    The main class you will be implementing. It uses `JSONFileIO` to save data. Note the existing `_load_data` helper and the empty method stubs.

6.  **test/store/test_json_file_io_unit.py** & **test/store/test_link_store_unit.py**  
    Examples of how to unit test these classes using `unittest.mock` to isolate them from the file system.

7.  **test/conftest.py**  
    Configuration for `pytest`. Notice how it handles the `--integration` flag to skip slow tests by default.

8.  **AGENTS.md**  
    When you get to the steps that ask you to use the copilot agentic AI while working in this repo, this file will be added to the context window of all interactions. This file gives an agent key context for successfully contributing to the file.


## 2. Implementation and Testing Steps

Follow these steps to complete the assignment.

!!! warning "Required `git` Commit Workflow for this Task"

    Work for **EVERY STEP** below must be done on its own branch!

    For **steps 1 and 2 specifically**, add your failing unit tests (not yet implementing the method) and make a commit with message (e.g. for step 1 "test: LinkStore.list() unit test failing"). Then implement `LinkStore.list()` and get to a green passing test. You should have 100% coverage when running the `run-qa.sh` script. Make a commit with this implementation (use a `feat:` prefix to the commit message and describe what you did). Finally, merge into `main`.

    There are seven steps in this task and each needs its own branch and merge commit!

    You are free to chose your own branch names, as long as they are descriptive, but if you'd like some conventional names here are some fine examples:

        1. `wip-linkstore-list-unit`
        2. `wip-linkstore-put-unit`
        3. `wip-linkstore-delete-unit`
        4. `wip-jsonfileio-persist-integration`
        5. `wip-jsonfileio-persist-unit`
        6. `wip-linkstore-integration`
        7. `wip-fixture-refactor`

### Phase 1: `LinkStore` - Unit Test and Implement

In this phase, you will implement the logic in `LinkStore`. **Do not edit `JSONFileIO` yet.** We will mock the persistence layer to ensure our logic is correct without relying on real files.

#### **Step 1: Implement `LinkStore.list()`**

You are practicing test-driven development in this step. Implement your unit test(s) for `list` and implementation _without copilot agentic assistance_. Be sure your test(s) for `list` _fail_. Commit your failing tests following the instructions in the notice box above titled "Required `git` Commit Workflow for this Task".

Now that you have failing test(s), work on improving your implementation and getting it to a passing test.

Once you have passing tests and 100% coverage, try using a copilot agent to code review your unit test(s) and implementation of `list`, without making any direct changes to your code, and seeing if you agree with any critiques enough to use them. If there are critiques you are unsure of, use this as an opportunity to learn and reflect on your initial implementation or testing strategy. 

0. Establish a branch for this step.
1.  Write unit test(s) for `list()` in `test/store/test_link_store_unit.py`.
    *   Mock `JSONFileIO` to return some sample data.
    *   Assert that `list()` returns a dictionary with the correct `Link` objects.
    *   **Crucial:** Test that `list()` returns a *copy* or new dictionary, not a reference to internal state.
    *   Run the test to be sure it fails.
2. Commit your failing test(s)
3. Implement `LinkStore.list()` to pass the test. Be sure the `run-qa.sh` script runs successfully and has 100% coverage.
4. Commit your passing test(s).
5. Have copilot perform a code review of just your implementation and tests and act on any suggestions you believe improve your code after investing the time and thought to understand them.
6. Make a final commit (if needed).
7. Merge back into `main` with a merge commit.

#### **Step 2: Implement `LinkStore.put()`**

Follow the exact same process for implementing the `put` method as you did the `list` method above. Write your initial test(s) and implementation _without_ the assistance of the copilot agent.

0. Establish a branch for this step.
1.  Write a unit test for `put()` in `test/store/test_link_store_unit.py`.
    *   use `Link` model to create a valid link.
    *   Call `put()`.
    *   Verify that the internal state is updated.
    *   **Crucial:** Verify that `self._storage.persist()` was called with the correct data. You may need to inspect how [`link.model_dump()`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_dump) works in [Pydantic documentation](https://docs.pydantic.dev/latest/concepts/serialization/#pydantic.BaseModel).
    *   Run the test to be sure it fails.
2. Commit your failing test(s).
3. Implement `LinkStore.put()` to pass the test.
4. Commit your passing test(s). Be sure the `run-qa.sh` script runs successfully and has 100% coverage.
5. Have copilot perform a code review of just your implementation and tests and act on any suggestions you believe improve your code after investing the time and thought to understand them.
6. Make a final commit (if needed).
7. Merge back into `main` with a merge commit.

#### **Step 3: Implement `LinkStore.delete()`**

For this step, you will gain experience working with a coding agent to help you draft unit tests that fail, before drafting an implementation that passes. You are following the same workflow as above, however, this time your goal is to have copilot write unit tests that fail first, _you_ review them and be sure the fail, then have copilot draft an implementation.

0. Establish a branch for this step.
1. Prompt copilot write a unit test for `delete()` in `test/store/test_link_store_unit.py` without modifying the implementation of `LinkStore.delete` because you want the tests to fail first.
    * Be sure copilot does not implement `delete`'s functionality yet. If it does, revert the implementation and reject that change.
    * Audit the test function(s) copilot generated and convince yourself they are correct and make sense. If you cannot, try getting to a point of feeling convinced whether that is through editing them yourself, attempting one more generation, or rewriting yourself by hand.
    * Delete should persist the changes via JSONFileIO (similar to how `put` does).
    * Run the test to be sure it fails.
2. Commit your failing test(s)
3. Prompt copilot to implement `LinkStore.delete()` and run the qa script until all tests pass with 100% coverage.
4. Review the implementation. Modify and/or improve upon it if needed. Run the QA script yourself to convince yourself of any changes you made.
5. Commit the passing implementation(s).
8. Merge back into `main` with a merge commit.

### Phase 2: JSONFileIO Persistence - Integration then Unit Tests

Now we will implement the actual JSON file writing capability.

Rather than implementing unit tests for `JSONFileIO` first, which will require `patch`'ing underlying behavior, it is actually more productive to 

#### **Step 4: Integration Test and Implementation for `JSONFileIO.persist()`**

Write this integration test without agentic assistance. Searching the web or engaging an LLM chat _with curiosity_ is fine, as needed.

0.  Establish a branch for this step.
1.  Open `test/store/test_json_file_io_integration.py`.
2.  Write a AAA test for `persist` marked with `@pytest.mark.integration`.
    *  Use the `tmp_path` fixture (provided by pytest) to create a temporary file path.
    *  Initialize `JSONFileIO` with this path.
    *  Call `persist()` with some data.
    *  Read the file back manually (using standard python functionality) and verify the content matches.
3.  Run `uv run pytest` (notice your test is skipped because it is marked as an integration test!).
4.  Run `uv run pytest --integration` (your test should fail, because `persist` is not implemented).
5.  Make a commit with your failing tests.
6.  Implement the `persist` method in `src/store/json_file_io.py`.
7.  Run the integration tests to be sure they pass. Run the QA script and be sure you have coverage.
8.  Make a commit with your passing tests.
9.  Engage with the copilot agent to code review your implementation and test. Act on any suggestions you understand and believe improve upon your first attempt.
10. Make a final commit, if needed.
11. Merge back into main with a merge commit.

#### **Step 5: Unit Test for `JSONFileIO.persist()`**

Now that you have a working implementation of `persist` that passes integration tests, your task moves to _unit_ testing `persist`. This will require a `patch` of the underlying file system functionality like we discussed in class. You should complete a first draft of this testing _without_ using copilot agent and can refer to the unit test for `load` for inspiration.

_Reflection question: Why might you want to add unit tests to `persist` even though you already have 100% coverage with integration tests?_ For some motivation, try running just your unit tests with a coverage report and see what you find:

* `uv run pytest --cov=src --cov-report=term-missing`

Since you already have a working implementation of `persist`, you cannot follow the red-green-refactor workflow of test-driven development. That's OK. You can work toward getting 100% test coverage with your unit tests _and this has value_ (you should be able to reason through _why_ it has value).

Rather than prescribing the exact set of steps here, go ahead and follow a branch/commit/merge workflow based on what we have done so far. Work toward writing _unit tests_ for your implementation of `persist` with a goal of reaching 100% coverage using the command above. Once you have a working implementation yourself, try using the agent to code review. Merge your work back into `main` with a merge commit when done.

### Phase 3: LinkStore Integration Tests

Finally, ensure `LinkStore` works with the real `JSONFileIO` instance via integration testing.

You **hopefully** cannot follow a red-green-refactor test-driven development pattern here and should be able to describe why not with confidence. That said, you should also be able to describe why this integration test will provide unique value to your test suite.

#### **Step 6: Integration Tests**

0. Go ahead and setup a branch for completing your integration testing of LinkStore. You should form commits regularly as you make progress.
1.  Working in `test/store/test_link_store_integration.py`.
2.  Add tests marked with `@pytest.mark.integration`.
3.  **Test 1:** Write a test that verifies `list` works with empty and non-empty initial files.
4.  **Test 2:** Write a test that verifies `put` works and persists the deletion. 
5.  **Test 3:** Write a test that verifies `delete` works and persists the deletion.
6.  Run the qa script to be sure all of your tests are passing.
7.  Merge your work back into `main` with a merge commit.

!!! question "Important Reflection Question"

    Think back to before these implementations were completed. Suppose you were tasked with implementing and testing `LinkStore` while your teammate is tasked with implementing and testing `JSONFileIO` at the same time.
    
    1. Why would _you_ start with unit tests?
    2. Why would your teammate start with integration tests?
    3. Why would it have been challenging for your teammate to start with unit tests on `JSONFileIO`?
    4. Generally, in future work, when testing, how would _you_ decide whether to start with unit or integration tests?
    5. Even though you had 100% coverage of `JSONFileIO` before adding 100% coverage with unit tests, and you had 100% unit test coverage of `LinkStore` before going back and adding integration tests, what unique value did those tests add, respectively?

    These are important concepts to feel develop some intuition and confidence in heading into the next quiz.

### Phase 3: Refactoring

#### **Step 7: Refactoring Tests with Fixtures and/or Helper Methods**

Perform a code review of the four files you modified in this task.

In the test files, look for redundancy in the **Arrange** step of your tests in a given file. Find at least one redundant set of steps and refactor those steps out to a fixture. Retest to confirm everything is still green, then form a new commit. You do not need to branch for this. **You must write and valuably use at least one custom fixture in your tests.**

Finally, go back and review your implementations of `LinkStore` and `JSONFileIO`. If there is any redundant code, refactor it out to a helper method. You may have already done this and, if so, there is no additional work to do here. If not, again test for coverage after the refactor, and make a commit (no branch needed). We will be looking to ensure no redundancy.

## 3. Hand-in

Hand in will open by Wednesday.

