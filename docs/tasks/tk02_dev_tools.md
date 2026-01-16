---
code: TK02
title: Implement a Dependency Manager ADR with an Agent
date: 2026-01-12
due: 2026-01-15
type: task
threads: ["SDE / ADR", "Tools / Code Agent"]
authors: [Kris Jordan]
---

## Prelude

In the alternate timeline, you previously submitted ADRs to Synercast.io. Chad selected you for the job!

> Subject: Welcome + First Engineering Task
> 
> Internal Memo: Welcome to SynerCast.ai!!!
> 
> From: Chadwick P. Ledger, CEO (HBS)
>
> To: Engineering (You)
>
> Subject: Welcome + First Engineering Task
> 
> Hi and welcome!!!
> 
> First off, congratulations on joining SynerCast.ai, one of the most exciting and futuristic companies in the software space right now. Our leadership team is made up almost entirely of Harvard Business School graduates, which means we think very strategically and also very big picture.
> 
> Earlier this year, we made the bold decision to offshore engineering to the cloud. The idea was simple: if AI can write code faster than people, why slow things down with engineers? This freed us up to focus on what really matters—vision, alignment, and pitch decks.
> 
> Honestly, for a while, it was going great.
> 
> Recently, though, we’ve noticed a few small things:
> 
> * The app only runs on my laptop.
> * Sometimes it runs, but the weather is for a different state.
> * Fixing one bug often creates a different bug, which we assume is just how software works now.
> * Nobody is totally sure which files are "the real ones."
> 
> So anyway, welcome! You are now the Engineering Department.
> 
> To keep things simple, we are starting small. Your first task is to help us "professionalize" how we manage dependencies.
> 
> Right now, installing the project is kind of vibes-based.
> 
> We would like you to:
> 
> * Decide on a proper Python package manager for the project.
> * Use the short Architecture Decision Record (ADR) you wrote in your application explaining that choice.
> * Implement the ADR you wrote yourself, by offshoring whatever you need to the cloud.
> 
> We’ve been told by several very confident people on the internet that all the coolest new companies in Silicon Valley are using something called **"uv"**, so that is probably the right answer. That said, we still need something written down that explains *why* we’re doing it this way, in case an investor asks.
> 
> You do not need to add features or redesign anything. We just want something we can point to and say, "Yes, we have an engineering process now."
> 
> If you could commit that ADR and make sure it says we chose **uv**, that would be perfect.
> 
> Thanks,
> Chad
> CEO, SynerCast.ai

## Getting Started

Get started by accepting the following GitHub Classroom Assignment: <https://classroom.github.com/a/3UMeYIjj>

!!! warning "Accept Invitation to Join COMP423 Spring 2026 Organization"
    After attempting to accept this first assignment, you may need to accept an invitation 
    to join our course organization. 
    
    To do so, in a different tab, log in to Github, navigate to <https://github.com/settings/organizations> and look for an invitation to join the organization.

Once your GitHub repository is created, you will need to clone it to your developer machine.

Open the project directory in VSCode. It should prompt you to reopen the project in a Dev Container. Accept the suggestion and wait for the dev container to download and install. Once it has, you should see "Dev Container: ..." in the bottom left corner of VSCode. All work in this course will be completed in Dev Containers.

## Commit, Branch, and Merge Expectations of this Task

A significant portion of this task's grade will be contingent upon following these `git` conventions.

1. You must create a branch named `adr001` and complete your work in that branch. Go ahead and do so. How can you verify you are on the correct branch?

2. You must commit your ADR, following guidelines below, in a single commit on your `adr001` branch with a commit message of `doc: add adr001 use uv for dependency management`. You can see an example of this for the [included ADR000 here](https://github.com/comp423-26s/tk02-starter/commit/bb2b420f6a20af610ab4102d987dfbb90e40c64b).

3. After reaching a point of generating configuration with an agent, reviewing it, and verifying its correctness, you will create a commit with message `feat: implement uv per adr001` with a _commit body_ that contains the agentic model you used as well as the prompt. If additional prompting is needed, document your understanding of what was wrong or unsatisfactory along with the subsequent prompt. All prompts and reflections should be included in the commit message. If you find more than 5 iterations are needed, you are encouraged to give up on this attempt (reset the commit) and try to improve your original prompt or try a different underlying model. For an example of what such a commit might look like, you can see the [commit for feature ADR000 here](https://github.com/comp423-26s/tk02-starter/commit/be6ea5daba2f6e2516300fd7cd99a3d4bd7625f0).

4. Once you are ready to merge your branch, you should force a merge commit so that the history of this branch is clearly maintained. To do so, switch to `main` branch and merge your feature branch with the `--no-ff` flag. You can use the default merge commit message. Here's an example of [how this history looked in the started code](https://github.com/comp423-26s/tk02-starter/commits/main/).

## Your Initial Task

The project has no dependency manager in the dev container and a key dependency is missing! How can you know? Try running: `python3 src/main.py`. The library named `requests`, a popular Python library for making API calls, is not installed in Python's environment.

When you begin work on a new concept: branch. Go ahead and make the new branch described in Commit Expectation #1 above to begin working on `adr001`. You will add your written ADR from TK01 (in markdown), the one where you decided on `uv`, as an appropriately named markdown file in the `docs/arch` directory. Once you have created your ADR file and saved it, go ahead and make the commit as described in Commit Expectation #2 above.

After you've made that commit, your task is to setup this project with `uv` such that when a new dev container is created (or rebuilt) the `uv` package manager is installed in the dev container, configured, and dependencies are `sync`'ed ("synchronized" or _installed_). Since installing and configuring a dependency manager in a dev container contains some non-critical configuration knowledge, it is a reasonable task to work with the GitHub Copilot Agentic AI on. Based on the strategies discussed in LS02, you should open a new agent prompt for this task. 

!!! info "Don't forget to claim Copilot Pro"
    If you run into trouble prompting Copilot within VSCode, make sure you've claimed your Copilot Pro coupon! This is a separate step from accepting Github's Student Developer Pack. To claim your coupon, head to GitHub and navigate to your profile > Settings > Billing and Licensing > Education Benefits and follow the instructions, then restart VSCode for the changes to take effect.

Try crafting an agentic prompt that includes the following context:

1. Describes what you want the agent to do for you (hint: it's implementing your Architectural Design Record)
2. Include your ADR001 file as input context explicitly, by referencing it with the `#` (hashtag) file search feature
3. Some useful hints to consider using in your prompt:
    * Less is more when it comes to configuration, use adjectives to help describe "minimal", "simple", and "well documented"
    * Keep the focus of the task small: "Do not add any `uv` dependencies yet."
    * Indicate your level of familiarity with `uv` and ask it to walk you through its changes
    * Use a state of the art model like Claude Sonnet 4.5 or GPT 5.2

!!! warning "Do not rebuild your container until your agent task completes"
    The agent _should_ modify your project's `./devcontainer/devcontainer.json` file. As soon as it does, before the task actually completes, VS Code will surface a pop-up asking you to rebuild the container. Ignore it! You will be able to see that the agent task is still working through completing its attempt.

When the changes complete, it is your job to evaluate what was changed and understand the lines of code added to your project in the agent's first attempt.

You don't need a _deep_ understanding of each change, but you should have a _general_ understanding of what each change does. If you do not: it's a _golden_ opportunity to learn! Rather than muddying the context of your agentic chat (and spending premium model requests...), you are encouraged to explore through web searches or a separate AI chat in the web browser.

### Verify it Works with Acceptance Tests

Once you believe you have a general sense of the files and changes made, how will you know they actually work? By _verifying them_ and proving to yourself they work.

Developing a habit of asking yourself, *"how can I be confident my changes work,"* and testing your hypotheses, is fundamental to being a successful software engineer. You need to be confident your changes to a project work before submitting them for code review or to production. This was true before AI and even more true post-AI.

Since you are coming up to speed on `uv`, we provide some manual acceptance tests for you to move through in your dev container should be able to complete.

!!! warning "What to do when you encounter errors"
    Does a step in your verification process produce errors? That's a part of the process! First: deep breath.

    Begin by trying to make sense of the error output. This is another great place where modern AI tools can explain cryptic error messages and possible solutions. There is often something small and manually actionable once you understand the error.
    
    If you think you are in too big of a mess to fix and want to start over, perhaps with a more refined prompt or model, this is why we use git! Use `git status` to see the files changed. You can reset the changes to existing files and delete new files to try again. Start a new context for the agent (+ icon) if you start over.

First, try rebuilding your dev container via VS Code Command Palette **"Dev Containers: Rebuild Container"**. Does the container successfully rebuild? This is the first and most critical acceptance test.

Now that your dev container successfully builds, check to see if `uv` is installed in your shell. Open a new terminal in the dev container and try both: `which uv` and `uv help` and you should see output.

Now, let's test adding a dependency via `uv`. Before doing so, to understand what happens when a dependency is added, you should go ahead and open up your `pyproject.toml` file and look for its `dependencies` configuration variable. It should be empty (if it's not empty because a clever agent added `requests` for you, try `uv remove requests` first). Back in your terminal, try `uv add requests`. Notice the output in terminal and the changes in your `pyproject.toml` file. The top-level requests dependency was added to `pyproject.toml` and sub-dependencies were added to `uv.lock` (if you open it). All were installed. If you try running `uv sync` now, you will see that everything is installed.

Now, let's try running the program with `uv`'s managed environment: `uv run python src/main.py`. You should see the glorious Synercast.ai weather status for Chapel Hill printed. (If you see an error message regarding a timeout, that's an error on the server-side and not your fault. Try running again.)

Finally, if you look in the hidden `.venv` directory in your project, and the `lib64` directory within it, you will see the `requests` package. You can see the source code for `requests` within, starting from the `__init__.py` module. The `.venv` directory is where all of your projects dependencies are installed. When you run `uv run python` it ensures Python's "environment" includes your project's `.venv` directory with top priority so that it uses these packages before any operating system or default packages.

!!! info "How to add .venv to your path to avoid needing to use `uv run`"
    If you try running `python run src/main.py` you will see that the import error still exists. This is because your shell is not using the project's `.venv` directory in its `PYTHONPATH` so Python does not know to look in `.venv` to load dependencies first.

    The common way to fix this is to "activate" the virtual environment in a shell. To do so, use the `uv venv` command and accept the replacement of your `.venv`. Since it blew up your `.venv` directory, will need to resync: `uv sync`. Then, try ending this terminal session (trash can) and starting a new one. You should see a first line of `source ...path.../.venv/bin/activate` which is a script that registers your venv in your shell environment. You should also notice the project name as a prefix to the shell prompt. Now try running `python src/main.py` and you will see the script works without `uv run`.

    This is common to other dependency managers that make use of virtual environments, including Poetry.

Great work! Now all that is left is to make your commit per Commit Requirement #3 and merge without fast-forwarding per Commit Requirement #4. Then you'll want to push your changes to GitHub and submit your work to TK02 on GitHub.

## Questions to be able to answer following this task:

* Where do my dependencies live in the directory structure for a project with a Python virtual environment?
* What file states what my project directly depends on?
* What file pins the exact versions of direct and indirect dependencies in a `uv` project?
* What command ensures my installed dependencies exactly match the project's pinned dependencies?
* How do I add a new dependency to a `uv` project? How do I remove it?
* How do I run commands so I’m guaranteed to they use the `uv` environment?