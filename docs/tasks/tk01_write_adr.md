---
code: TK01
title: Write ADRs for Package Managers
date: 2026-01-09
due: 2026-01-11
type: task
threads: ["SDE / ADR"]
authors: [Kris Jordan]
---

# Task 01 - Write ADRs for Package Managers

## Prelude

In an alternate timeline, you applied for job with Synercast.io. One of about one hundred applications you submitted. They followed up!

> _From the Desk of Chad / Director of Talent Velocity & Strategic People Outcomes_
>
> Dear Future Synercaster,
> 
> First of all: congratulations. Not on getting the job — _not yet_ — but on being noticed. That alone puts you in what I like to call our **Top-of-Funnel of Destiny**.
> 
> At Synercast.ai, we don’t just hire people. We **curate potential**. We believe in **auditioning for excellence, pressure-testing curiosity**, and discovering fit through what we proudly call:
> 
> **The Pre-Hire Learning Engagement™**
> 
> This is not an interview.
>
> This is not unpaid labor.
>
> This is not _not_ unpaid labor.
> 
> **This is an opportunity.**
> 
> You’ve been invited to complete a short architectural thinking exercise that mirrors the kinds of decisions our engineers face early, often, and occasionally five minutes before a meeting that definitely could have been an email.
> 
> You will not be told the “right” answer.
> You will not be judged on trivia.
> We care far more about how you think than what you pick.
> 
> The detailed instructions live in the project memo that follows. It contains more nuance and technical specificity than I’m qualified to explain. I skimmed it, nodded a lot, and approved it.
> 
> Take this seriously. Don’t over-optimize. Write like someone else will have to live with your decision. Because they will. Possibly you.
> 
> Proud of you, already, _in a professional way_.
> 
> Synergistically yours,
>
> Chad
>
> Director of Talent Velocity & Strategic People Outcomes / Synercast.ai

## Pre-requisite Reading

You should read [RD05 - Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html) and complete the guided reading questions in Gradescope before starting with this task.

## Context

Modern software projects rely heavily on **package managers** to handle dependencies, environments, and reproducibility. In Python, this space has evolved rapidly, and multiple tools coexist with different philosophies and trade-offs.

In this assignment, you will explore **two modern Python package manager strategies**: **Poetry** and **uv**. You will practice making decisions under uncertainty.

Rather than "picking the right tool," the goal is to:

* understand *why* teams might choose one approach over another,
* practice reading real documentation,
* engage an LLM as a learning tool _with curiosity_, **not** with laziness,
* and document decisions using **Architectural Design Records (ADRs)**.

You will ultimately submit **two ADRs**:

* one that justifies choosing [**Poetry**](https://python-poetry.org/)
* one that justifies choosing [**uv**](https://docs.astral.sh/uv/)

Each assuming a plausible but different project context.

## Learning Objectives

By completing this assignment, you will gain experience with:

1. Writing **Architectural Design Records (ADRs)**.
2. Reading and extracting meaning from **open-source documentation**.
3. Understanding the **role of package managers** in Python projects.
4. Using an **LLM to learn unfamiliar technical concepts** and clarify trade-offs.
5. Reasoning about **diverging project paths** where multiple choices are defensible.

## Your Task

### Part 1: Learn the Landscape (Research & Exploration)

You should develop a working understanding of:

* What problems Python package managers aim to solve
* How **Poetry** and **uv** approach those problems differently
* What kinds of teams or projects might prefer each approach

You are encouraged to:

* Read official documentation
* Skim README files and "Getting Started" guides
* Use an LLM to ask clarifying questions, generate summaries, and test your understanding

> ⚠️ **Important**: If you use an LLM, you are still responsible for verifying claims against documentation. Treat the LLM with a healthy dose of skepticism, not an absolute authority.

#### Guided Questions You Should Answer Before Writing ADRs

You will not submit responses to these questions, but you should be able to answer the following questions *in your own words* before writing the ADRs. These questions are designed to guide your research into learning about package managers and poetry/uv.

1. What core problems do package managers solve in a Python project?
1. Why is dependency versioning essential for reproducibility?
1. What risks or symptoms arise when dependencies are not managed consistently across environments?
1. How does a lockfile differ from a dependency specification file, and why does that distinction matter?
1. What is the purpose of a virtual environment in Python?
1. How do environment isolation and dependency management relate, but differ?
1. What challenges arise when multiple Python projects coexist on the same system?
1. How does Poetry encourage reproducible builds, and what trade‑offs does that approach introduce?
1. What problem space is uv primarily trying to optimize for, and how does its approach differ from all‑in‑one tools like Poetry?

### Part 2: Write Two ADRs (Decision Documentation)

You will write **two short ADRs**, each making a different decision:

* **ADR A**: Decide in favor of **Poetry**
* **ADR B**: Decide in favor of **uv**

Each ADR should:

* Assume a *reasonable but distinct project context*

  * (e.g., a student team project, a production service, a fast-moving prototype, a research codebase)
* Explicitly acknowledge trade-offs
* Be internally consistent and defensible

> The goal is *not* to argue which tool is "better," but to show that **both choices can be correct under different constraints**.

#### Example ADR for a DevContainer

To give you a sense of what a reasonable ADR might look like for another similar decision, here is an example, representative ADR that supports the decision to use DevContainers for a reproducible development environment:

~~~.markdown
# ADR00: Standardize Python DevContainer

## Context

This project needs a predictable and reproducible development
environment.

Team members have machines capable of running Docker containers, and
we want a development setup that can also be used in hosted or
cloud-based development environments.

Several forces are in tension:

- We want onboarding to be fast and reliable for new contributors.
- We want local development to match CI closely to reduce
  environment-specific failures.
- We want to minimize maintenance work for the team over time.

## Decision

We will use VS Code Dev Containers with a standard,
Microsoft-maintained Python base image.

We will keep the DevContainer definition lightweight by preferring
configuration over customization and only add project-specific tooling
when it is necessary.

We will use a standard Python .gitignore so temporary files, build
artifacts, local environments, and secrets are not committed.

## Considered Options

- We could run directly on the host OS using a `venv` (or similar).
  This reduces container overhead but increases variability across
  developer machines.
- We could build and maintain a custom Docker image. This gives more
  control but increases the maintenance burden.

## Consequences

- New contributors can start development by opening the repository in
  he container, which reduces setup steps and configuration drift.
- Development and CI are more likely to use the same tooling
  versions, which can reduce “works on my machine” failures.
- The project depends on Docker and VS Code Dev Containers, which may
  add friction for developers who cannot or prefer not to run
  containers.
- Running in a container can reduce performance compared to running
  irectly on the host OS, especially for file-heavy workflows.
- Using an off-the-shelf base image reduces ongoing maintenance but
  limits customization to what the base image supports.
~~~

#### ADR Expectations

Each ADR should be **~½ to 1 page** and include the following sections:

1. **Title**
3. **Context**
    * What kind of project is this?
    * What constraints or priorities matter?
4. **Decision**
    * What tool is being chosen and why?
4. **Considered Options**
    * What alternatives were evaluated?
5. **Consequences**
    * What are the benefits of this choice?
    * What are the costs or risks?
    * What might be harder because of this decision?

You may reference:

* Documentation
* Reasoning informed by LLM conversations
* Comparisons to alternative approaches

## Hand-in on Gradescope

You will submit your two written ADRs for this Task on Gradescope.