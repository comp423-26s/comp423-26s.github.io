---
code: TK07 
title: "Refactor Persistence Layer to an SQLModel"
threads: ["System / RDBMS"]
authors: ["Kris Jordan"]
date: 2026-03-06
due: 2026-03-13
---

# Migrating to an ORM

## Overview

In this assignment, you will replace the URL shortener's temporary flat-file persistence layer with a real PostgreSQL-backed persistence layer built with `SQLModel`.

This is an individual assignment, not a paired assignment.

We are providing a working starting point for your TK07, however a 5% extra credit opportunity does exist if you migrate your TK06 project independently. See the section on extra credit for more information on how to take this on.

The standard setup for this task already has a minimal working implementation for layers you have completed in earlier tasks:

1. a FastAPI API with request/response models
2. a service layer
3. a `store` layer that persists data to a JSON file

Additionally, this task has working configuration for getting started with PostgresQL integration. Namely, we supply:

* The `engine` and `session` in `db.py`
* A viable `SQLModel` for the `Link` type in `entities/link.py`
* A database reset script in `util/reset_db.py`

## Learning Objectives

After completing this assignment, you should be able to:

1. Refactor an existing layered application to replace an underlying layer.
2. Use `SQLModel` entities, sessions, and queries in a service-oriented design.
3. Distinguish API-facing models from persistence entities.
4. Design integration tests that verify real database behavior.
5. Remove obsolete layers and tests once a new architecture is in place.
6. Work incrementally in Git branches rather than making one large risky change.

## Required Outcomes

By hand-in, your project must satisfy **all** of the following:

0. **Do all work in branches along the way.**
1. **Completely remove the `store` code layer and its respective tests.**
2. **Implement the service layer in terms of `SQLModel` sessions.**
3. **Fully test the session layer integrated with the database.**
4. **Have working end-to-end tests and integration tests for routes.**
5. **Pass all QA gates in `scripts/run-qa.sh`.**

The layers of your implementation should remain cleanly separated:

- routes handle HTTP concerns and API models handle request/response validation
- services handle business logic and persistence coordination,
- entities model database tables.

You must have 100% test coverage upon hand-in.

Finally, of course, you must be able to walk through your feature from start to finish on your development server. This means starting the server, navigating to the OpenAPI `/docs` tool, creating a link with a vanity slug, successfully accessing that link's slug from a web browser and being redirected, and finally listing all active links and seeing your link created. Additionally, all edge cases for this limited scope of functionality should remain functional, such as navigating to a slug that does not exists 404s.

## Important: Getting Started

**Everyone needs to seed a new, empty repository with your TK07 starter code.**

Everyone needs to accept the TK07 GitHub Classroom assignment here: <https://classroom.github.com/a/FZKooMTH>

This repository will initially be empty. If you have trouble accessing it, be sure you have accepted the invitation via GitHub.

### Standard Setup

If you were in class on Friday, March 7th, you should have already cloned and setup the tk07 starter repository. What you need to do is replace the `origin` remote with your personal `tk07` remote. Step-by-step: _remove_ the existing `origin` remote, this was the URL you cloned in class, and add a new remote named `origin` that points to your assignment repository. Go ahead and push `main` to this new `origin` and confirm you are seeing the starting point on GitHub.

### Extra Credit Setup

If you are pursuing the extra credit option of retrofitting your TK06 project with the ORM layer, you will need to carry out a similar set of steps as the standard setup, but from your local TK06 repository instead. Remove the `origin` remote from your TK06 repository and then add a new `origin` remote pointed at your empty TK07 repository. Go ahead and push your TK06 there to test the git remote setup. 

## Suggested Workflow

There will be broken tests and functionality while you endeavor to replace the storage layer of the stack. A general strategy here is much like a remodeling project: start with some demolition that is broken but ready for rebuilding and then work step-by-step with testing and verification along the way.

1. Create a branch for this task
2. Create another branch for each step you take
3. Steps to consider:
    - Remove the `store` layer implementation and tests
    - Choose one service method to try and make work (hint: reads tend to be easier than writes, so `list_links` is likely the easiest place to start).
    - Try implementing the method first and trying it out in the dev server to convince yourself it is working. Notably, this recommendation is _not_ following the test-driven development mantra of red-green-refactor (We are pragmatic, not dogmatic!). For inspiration, look toward the `orm-demo` project we explored in class and in your readings.
    - Once you believe you have it working via manual testing in the dev server, write your integration tests for just this service method. You may be well served to start a new test module rather than reuse the existing service test module since the arrange steps will be much different. Focus on getting these specific tests to pass and try not to be distracted by other tests that will fail while you are mid-refactor.
    - Once you have a method working and tested, continue on to the next method until the service layer is fully integration tested.
    - Commit the work to this step's branch, then merge the work back into your task branch
4. Once you have completely tested the service layer, your routes should work! Try it out in your developer server. However, the tests for those routes need to be revisited. **There is one fundamental, big lesson to appreciate here!** Think about _why_ your routes still work without any further changes, though some of the tests for those routes _do_ require changes. Make a branch for fixing the routing tests that are broken, fix them, and merge back in.
5. Finally, once you are ready for submission and have verified you have met the requirements listed in [Required Outcomes](#required-outcomes), merge your task branch back into `main` and push to your TK07 repository.

## Resources

The readings, in-class work, and demo repositories are meant to serve as primary resources and documentation for helping you navigate this work. For this task, we recommend trying to do it by hand and without AI. There are very valuable lessons to learn in what it takes to undergo a refactoring process like this. Once you have a strong handle on those lessons, which is only really obtained through practice, then this is the type of task an AI coding agent can help do some of the mechanical work on.

## Extra Credit (5%)

If you successfully retrofit your TK06 solution to meet the required outcomes, you are eligible for 5% extra credit. You should only take this on if you have a high degree of confidence in your TK06 design choices and solution. You will be responsible for migrating your repository over to Docker Compose, setting up the postgres configuration and database infrastructure, and so on. You can, and probably should, look toward the `orm-demo` repository for an example of how to do this.