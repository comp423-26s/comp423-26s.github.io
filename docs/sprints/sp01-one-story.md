---
code: SP01
title: One Story End-to-End
date: 2026-04-09
due: 2026-04-19
type: sprint
threads: ["Design"]
authors: [Kris Jordan]
---

# Sprint 1 - One Story End-to-End

The goal of this sprint is to have your primary story working end-to-end in the LearnWithAI codebase. Additionally, your team will get into the flow of performing Pull Requests and Code Reviews for one another and keeping your project board updated to reflect the status of ongoing work.

## Expectations

* One story end-to-end
* Project Management Standards
* PR/CR Workflow Enforced from `main`

## Your Primary Story

Focus on your team's most valuable user story. Your goal is to have this working and interactive from the front-end all the way to the back-end. In this first week, your focus is orienting yourself with existing code and finding where your team's work will fit into it. Since this is a larger code base than in most prior courses you have taken, you can find examples of most things are trying to accomplish by a combination of (a) looking around at other areas of the application and (b) engaging with curiosity using an agentic AI.

### Back-end API and Data Models

Your team should likely start with establishing your back-end Pydantic models and routes.

For now, we recommend establishing your team's own separate router file in an appropriate `api` subdirectory. Start with a single test route to be sure you can get it working and showing up in the `localhost:8000/docs` OpenAPI interface. After defining a router and adding a route to it, be sure to register it in `api/src/api/main.py`. Before continuing further, be sure you see your route appear in `/docs`.

Helpful hints:

* To run the development servers there are two common paths:
    * As a Task: Command Palette > Run Task > dev: run frontend + api + job queue
    * Debugger: Debug Pane > Debug Profile Selector > Debug Frontend + API + Job Queue
* When in doubt, reset your database following the steps in `README.md`
    * The script to reset data: `uv run python3 packages/learnwithai-core/scripts/reset_database.py`

Once you have a "hello world" route that you can successfully use from `/docs`, you are ready to start fully defining the routes you will need for this story. For now, we recommend focusing only on the routes you need for your initial story and no more. These routes will also need Pydantic models, or changes to existing models.

New models should be added to new files in the `api/models` directory. If you need to "modify" an existing model, we recommend the approach you take for now is to use inheritance to define a new model just for your feature which extends the existing model and adds any additional fields needed.

The FastAPI routes you define and need for this story should follow the conventions we learned about annotating route parameters this semester for API documentation purposes. You should also include documentation for your route definitions like we expected during the FastAPI exercise earlier this semester.

**To regenerate frontend API bindings based on your updated API definitions, you can start a terminal in the `frontend` workspace of the project and run the command `pnpm api:sync`.** The API bindings in the frontend are generated from the API you define in the backend via FastAPI thanks to its ability to produce OpenAPI specifications.

### Back-end Services

Your routes should handle HTTP-level concerns, but ultimately should delegate the business logic to a service with necessary inputs coming from the request.

You should define a new service similar to how other services are implemented in `core/src/learnwithai/services`, as well as `tools/jokes/service.py` and `tools/activities/iyow/service.py`, also appropriately organized in the file structure, with the service methods your routes will depend on. 

### Front-end

How your team's front-end is organized will be highly dependent upon your feature and story. You should find your way to the components you are likely to integrate with. It is likely you will want entirely new front-end router; to see how this is accomplished, take a look at how other features work in the codebase and find relevant examples to work off of. 

Since frontend web development is more the concern of COMP426, and state of the art modern AI Agents are available to you , we expect most teams' frontend code will involve significant generative assistance.

In the GitHub Student Developer Pack with Copilot Premium opt-in, we recommend using GPT-5.2-Codex with high thinking when you are taking on significant agentic tasks. It is capable of producing high quality frontend code, writing and running tests, helping debug, and more. Even if you have taken COMP426 or have prior experience with Angular, we encourage using this opportunity to practice working with an agent to produce frontend code.

Branching early and committing often will help you avoid digging a hole you can't get back out of when using an agent to implement an ADR or plan that you have written for front-end functionality.

If you arrive in office hours with code for your feature which you cannot explain, the TAs are instructed to help you revert back to a working commit, or your `main` branch, and ask you to try starting over while thinking about strategies for working on a smaller task at a time.

## Team Project Management

You are expected to utilize the project management tools of a GitHub Project Board, Issues, and PRs for the remaining sprints of the course:

1. Maintain your Project Board with cards linked to issues, assigned to team member(s), with descriptive titles for all cards/issues
2. Perform work on branches off of `main`
3. Perform pull requests with well written titles and messages and request code reviews from team members
4. Make effortful and helpful code reviews for your team mates, helpfully maintaining high standards of code
5. Merge approved PRs into `main` with merge commits

## PR/CR Settings

Let's setup your GitHub repository!

One member of your team should accept the project on Github Classroom and **name your team "Team A1"** (replace A1 with your assigned table in Carroll): <https://classroom.github.com/a/gsibDpyK> - double check your table to be sure you do not accidentally create the wrong team name. Other members of the team should join this team.

Everyone on the team is encouraged to setup branches to avoid confusion:

1. Remove the `origin` remote (`git remote rm origin`)
2. Establish your team's repository as the new `origin` (`git remote add origin <your repo>`)
3. Establish the official repository as `upstream` (`git remote add upstream https://github.com/unc-csxl/learnwithai.unc.edu.git`)

A member of the team should setup the branch protection rules for `main` in your team repository. In your team's final project repository, navigate to:

1. Settings
2. Go to Branches and add branch Ruleset
    1. Ruleset name: `main`
    1. Enforcement status: `Active`
    1. Targets, Add Target, select **Include default branch**
    1. (Check) Restrict deletions
    2. (Check) Require a pull request before merging
        1. (Check) Require approvals: 1 required
        2. (Check) Dismiss stale pull request approvals when new commits are pushed
        3. (Check) Require approval of the most recent reviewable push
        3. (Check) Require conversation resolution before merging
    3. (Check) Require status checks to pass
        1. Add Check, search for `qa` and add it
    6. Save Changes with `Create`

Your team repository now protects `main` from modifications and requires Pull Requests, Code Reviews, and passing Continuous Integration to merge back into `main`. This workflow is representative of many industrial workflow settings.

## Project Board

Agree on **one** member of your team should establish a project board for your team.

1. Begin by opening you your team repo page on GitHub. 
2. Be sure you do this **from your team's repository page**! From this page, click the `Projects` tab. Click `New Project`. 
3. From the pop-up with templates, select `Featured` and then select the `Kanban` template. 
4. Name the project "Team XN Project Board", where XN is your table. 
    1. Uncheck the box "Import items from repository"
5. Finally, press the ellipses `...` in the top right corner, beneat your profile photo, and select **Settings**. 
6. Click **Manage Access** and under "Invite Collaborators", search for your team, select it, make the role Admin, and click Invite.
5. After completing these steps, other members of your team should verify they are able to access the team project board by going to the repository on GitHub, clicking the Projects tab, seeing the project show up there and able to navigate to it.

Toward the end of project management expectation #1, Maintain your Project Board with cards linked to issues, assigned to team member(s), with descriptive titles for all cards/issues, here is what we will look for in the grading of this sprint:

1. All project board titles are descriptive
2. Some cards are in states beyond the Backlog/Ready columns (and accurrately reflect progress)
3. All cards beyond Ready are assigned to one or more specific team members
4. All cards beyond Ready are linked to a Github Issue

We will discuss project boards on Friday 4/10.