Note that we are implementing a store that is not very scalable or generally best practice. We are choosing it because it has clear boundaries and highlights some of the fundamental testing concerns that exist in a larger system where a data store is implemented with a much more sophisticated system (such as a relational database or key-value storage engine).

Try running tests in tests explorer (and try it with coverage button!)

Students should go through a guided code read (with GRQs):
  * README.md
  * scripts/run-qa.sh
  * models/link.py
  * store/json_file_io.py
  * store/link_store.py
  * test/store/*
  * conftest.py
  * AGENTS.md

Follow a very specific simple get routine: switch to a wip-branch for the feature, implement the feature, continue.


# Implement LinkStore methods and unit test (with mocking!) to avoid dependency on underlying JSONFileIO

NOTE FOR KRIS: Update descriptions of methods in assignment to be more precise on expectations (list must not expose internal state or produce a mutable reference as a return value to the caller).

Requirement: do not change `JSONFileIO` during this process!!! Do not integration test `LinkStore`!!!

* Start with implementing `LinkStore#list` *unit test only, mock persistence concerns.*
    * Must not expose external state or offer a mutable reference as a return value to caller
    * Start with doing this one by hand.

* Continue with testing `LinkStore#put` *unit test only, mock persistence concerns.* 
    * Try having the AI help with this one and _very closely audit every line of source code and test code it produces.
    * We may need to hint at what `JSONFileIO#persist` expects and how `link.model_dump()` works in Pydantic.

* Continue with testing `LinkStore#delete` *unit test only, mock persistence concerns.* 
    * Try having the AI help with this one and _very closely audit every line of source code and test code it produces.

Your implementation of `link_store` should not have any duplicated logic in its methods. Please refactor duplicated logic into a well named helper method with a prefix underscore. See `LinkStore#_load_data` for an example.

## Implement JSONFileIO persist method with an integration test to verify first

Integration test must be marked as such; confirm by running regular unit test suite and seeing that your test is skipped.

Integration test should make use of `tmp_path` fixture in pytest.

Add unit tests to JSONFileIO Persist. Here you will need to patch behavior. You may need to know about json.dump (link to standard library).

## Implement Integration Tests with LinkStore

Add one integration test that verifies list works after loading data

Add one integration test that verifies put persists

Add one integration test that verifies delete persists

Organize redundant arrange code into a fixture