---
code: TK04
title: Professionalizing the Developer Environment
date: 2026-01-22
due: 2026-01-27
type: task
threads: ["SDE / ADR", "Tools / Code Agent"]
authors: [Kris Jordan]
---

## Prelude

In your alternate timeline, you received the following email.

> Internal Memo: The Company Has Discovered "Standards"
> 
> From: Chadwick P. Ledger, CEO (HBS)
>
> To: Engineering (You)
>
> Subject: Congratulations, You Now Own "Quality"
> 
> Hi and welcome back!!!
> 
> First off: outstanding work on the last task. I personally watched the terminal print weather for Chapel Hill, and I immediately forwarded a screenshot to three investors with the caption: "We are basically profitable." This is what we at SynerCast.ai call "traction" and "validation". That "timeout" was _definitely a fluke."
> 
> Now that we have solved dependency management, leadership is ready to take the next strategic leap forward: we are professionalizing. I know it sounds intense, but please remember: professionalism is just vibes, except you can run it in the command line.
> 
> Here’s the situation. We’ve noticed an alarming trend where code is being written in multiple styles, bugs are being introduced without any formal announcement, and the app sometimes works only if you believe in it hard enough. This is a risk to our brand, our roadmap, and most importantly, Chad’s ability (me) to demo things live without sweating through a quarter-zip.
> 
> So your next mission is simple: add the kind of automated guardrails that make a project feel like it belongs to a real company. Think: consistent formatting, helpful warnings before mistakes become folklore, and a way to prove things work that doesn’t involve "it ran once on my machine."
> 
> Thanks in advance.
> 
> Warmly,
>
> Chadwick P. Ledger, CEO (HBS)
>
> SynerCast.ai



## 1. Overview

In **Task 2**, you established the foundation of your project by selecting **`uv`** as your dependency manager and automatically installing it in your Dev Container. 

For this task, we are moving from a "functioning" project to a "professional" one. You will extend your developer tooling to include automated guardrails that ensure code quality, consistency, and correctness. You will again write **Architectural Design Records (ADRs)** in your own words to justify your choices and use **Generative AI Agents (GitHub Copilot)** to implement them following a specific `git` workflow.

Your work in this task will follow your work in Task 2 and reuse the same git repository and dev container.

## 2. Technical Aside: Dev vs. Production Dependencies

In modern projects and dependency managers, it is critical to distinguish between what your **app** needs to run and what **you** need to build it or actively work on it.

* **Production Dependencies:** Packages required for the code to run in the hands of a user (e.g., `requests`).
* **Development Dependencies:** Tools used only during the development process (e.g., `pytest`).

**Why it matters:** Including testing tools in a production environment increases the size of your deployment and creates unnecessary security "attack surfaces." 

> **Action:** When adding these tools, always use the `--dev` flag:
> `uv add --dev <package_name>`

After doing so, take a look in your `pyproject.toml` file to see how development dependencies are specified.

**All of the dependencies added in this task are development dependencies and should be installed as such.**

## 3. The Quality Stack Requirements

For each of the following three categories of tools, you will establish a new branch, perform some research, write an ADR with a specific commit, and then implement the ADR following another commit, verify your solution works, then merge your work back into main with a merge commit. Whereas in Task 2 we were lenient on this workflow, in this task we will expect comfort with the workflow and it will be a substantive portion of this task's grade.

## 4. The Strict Git Workflow

We were lenient on Git discipline in Task 2. For this task, **the workflow is a core part of your grade.**

1.  **Create a Feature Branch:** Branch off `main` (e.g., `adr002`).
2.  **Research & Commit ADRs:** Decide on your tools. Write your ADRs in `docs/arch/`. **You must commit these ADRs to your branch before writing any implementation code with a `doc: ` prefix.**
3.  **Engage the Agent:** Use GitHub Copilot (Agent Mode). Provide the ADRs as context and ask the agent to:
    * Install the tools as **Development Dependencies** using `uv`.
    * Configure the devcontainer (`.devcontainer/devcontainer.json`) to enable the tools.
    * Produce as simple and straightforward of an implementation as possible, like a senior software engineer.
4.  **Verification:** Perform the manual and automated checks. When you face failures, you will need to investigate and learn where they are coming from.
5.  **Committing Feature Work:** Once your work is verified, you will create a `feat: ` commit like in Task 02 that contains the prompts and models you used, as well as any insights or commentary on what you noticed when astray.
6.  **The Intentional Merge:** Merge your branch back into `main` using an **explicit merge commit**:
    ```bash
    git merge --no-ff adr002
    ```
    *We will be checking your Git graph for the "diamond" shape created by this merge.*

### A. ADR002 Source Code Formatting & Linting

Before writing your ADR, you should read an overview of each of the tools and be able to answer the following questions:

* What is a code formatter?
* What is a linter?
* What value does each uniquely provide to a software engineering team?
* What plugin(s) exist in VSCode to automatically run these tools on your files when you save them?

Tools to investigate and choose from:

  1. `black` and `pylint`
  2. `ruff`

For this `git` branch, name it `adr002`. Add your second ADR in the `docs/arch` directory. Make a commit with `doc: ...` as the prefix and complete the commit line with appropriate description (replacing `...` with a meaningful title). When you get to implementing the ADR, setting up your project with these tools, you will ultimately produce a `feat: ...` commit with a descriptive subject line and a commit body that includes the models and prompts you used, as well as the iterations it took, as was expected in Task 02. This time it is on _you_ to verify it works with acceptance tests. The things you should verify before merging, and continue iterating on until you can, are:

1. Your tool(s) work in the command-line
2. Your tool(s) are automatically run in VSCode when you save a file. For this verification, you have the burden of figuring out how to convince yourself it is working. This may require a VSCode plugin and some configuration which can be installed and configured in the devcontainer via your devcontainer.json file.
3. Both of the above are verifiable _after_ rebuilding your devcontainer.

Finally, update your project's `README.md` to have a section that covers "Formatting and Linting" with instructions on how to run the tools. This is a task I would encourage experimenting with Agentic AI help on... _but remember that you own output's correctness and readability_!

Once you have made your `feat:` commit with a verified implementation, merge it into your `main` branch with a merge commit.

### B. ADR003 Static Type Checking

Before writing your ADR, you should read an overview of each of the tools and be able to answer the following questions:

* What is a static type checker?
* Why is a static type checker useful in Python?
* Why don't you need a separate tool for this in a language like Java?
* What plugin(s) exist in VSCode to automatically run these tools and highlight type checking errors in your editor?

Tools to investigate and choose from:

1. `mypy`
2. `pyright`

For this `git` workflow, follow the same naming conventions, standards, and expectations as the previous ADR. It will be on you to determine how to verify the tool you choose works in your devcontainer and vscode IDE integration. We will ask you to be able to prove this verification in the submission for this task.

### C. ADR004 Testing & Coverage 

Before writing your ADR, you should read an overview of each of the tools and be able to answer the following questions:

* How much boilerplate ("ceremony") is required to write a test in this framework?
* What support does this testing framework have for extensions (like code coverage)?
* What support does this testing framework have for _fixtures_? What are the developer ergonomics?

Tools to investigate and choose from:

1. `pytest` and the `pytest-cov` plugin
2. `unittest` combined with `coverage.py`

For this `git` workflow, follow the same conventions as earlier ADRs.

To verify that your chosen tools are working in your dev container, you will need to add at least a basic, example test file to the repository. An agent can be helpful here, but use any agentic code to understand how it comes together! It's OK if it does not have 100% coverage of `src/main.py`, the important quality is that the tests run and you can see some coverage report of `main.py`.

To verify your chosen tools work in VSCode, you should be able to run your tests from the VSCode testing pane.

## 6. Guiding Questions for Exploration

Use these questions to help formulate the **"Forces"** and **"Decision"** sections of your ADRs:

1.  **Unified vs. Modular:** Does a single tool reduce configuration "toil" compared to using multiple specialized tools?
2.  **Boilerplate:** Compare the code needed to write a test in `unittest` versus `pytest`. Which feels more maintainable for a growing team?
3.  **Developer Velocity:** Does a faster type-checker like **Pyright** provide enough of a productivity boost to justify moving away from the industry-standard tool like **mypy**?