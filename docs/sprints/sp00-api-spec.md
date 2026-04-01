---
code: SP00
title: "Technical Specificiation of Data Tables and API"
date: 2026-04-01
due: 2026-04-06
type:  reading
threads: ["System / APIs"]
authors: [Kris Jordan]
---

# Sprint 0 - Week 1 - Technical Specification

Now that your initial user-centered feature design document and mid-fi wireframes are in place, your team will extend your work by thinking through your database model and HTTP API to support it. 

This is an exercise at thinking at different layers of abstraction: we've prioritized the most important one which is what value you are trying to provide to a user. Next, you'll go all the way down to the bottom of the stack and think about your data model. Fred Brooks has a famous quote about specifying data tables in technical specs:

"Show me your tables and I won't usually need your flowcharts; they'll be obvious." -Fred Brooks (1975)

Finally, you will bisect the layers and think about your API design which rests between your frontend user-interface and the backend.

## Assignment Details

You will extend your design document to add a technical specification section. The technical specification section will have database modeling.

### 1. Database Modeling

Your feature will need its data persisted in the PostgresQL database, with modeling in SQLModel entities. To help give an example of what simple feature tables can look like, here are some starting points. 

#### Tool Example Table

The very simple demo Joke Generating Tool is backed by a table that looks as follows. Of course, many tool ideas would require more than one table:

**`joke_tool__joke` table** - the persisted data about joke prompts and geneted responses

- `id` (int, PK, autoincrement)
- `course_id` (int, FK → course.id, NOT NULL)
- `created_by_pid` (int, FK → user.pid NOT NULL)
- `prompt` (text) the prompt the user requested to generate jokes
- `jokes` (JSON) - the list of generated jokes returned by the AI API
- `async_job_id` (int, FK → job.id, NOT NULL)
- `async_job` (relationship to the AsyncJob)
- `created_at` (datetime with tz, server default now)
- `updated_at` (datetime with tz, server default now, onupdate)

#### Student Activity Structure

If you are thinking about a student activity, here are the tables which will already exist in the code base. You will not modify these, but you will add one or more table(s) that relate to these:

**`activity` table** — shared metadata for all activity types:

- `id` (int, PK, autoincrement)
- `course_id` (int, FK → course.id, NOT NULL)
- `created_by_pid` (int, FK → user.pid, NOT NULL)
- `type` (varchar, NOT NULL) — discriminator string (e.g. `"iyow"`)
- `title` (text, NOT NULL)
- `release_date` (datetime with tz, NOT NULL)
- `due_date` (datetime with tz, NOT NULL)
- `late_date` (datetime with tz, nullable) — optional late submission cutoff
- `created_at` (datetime with tz, server default now)
- `updated_at` (datetime with tz, server default now, onupdate)

**`submission` table** — shared metadata for all submission types:

- `id` (int, PK, autoincrement)
- `activity_id` (int, FK → activity.id, NOT NULL)
- `student_pid` (int, FK → user.pid, NOT NULL)
- `is_active` (bool, NOT NULL, default True)
- `max_points` (float, nullable) — future use
- `points` (float, nullable) — future use
- `submitted_at` (datetime with tz, NOT NULL)
- `created_at` (datetime with tz, server default now)
- **Unique partial index: `uq_submission_active`** on `(activity_id, student_pid)` WHERE `is_active = True` — enforces at most one active submission per student per activity

If you imagine a simple demo AI student activity like "In Your Own Words" (IYOW) where an instructor creates a prompt for students and the students need to try and explain the prompt in their own words in their submission with some automated AI feedback, you could imagine feature-specific tables like the following:

**`iyow_activity` table** — "In Your Own Words" activity details:

- `id` (int, PK, autoincrement)
- `activity_id` (int, FK → activity.id, unique, NOT NULL) — 1:1 with base activity
- `prompt` (text, NOT NULL) — the question/prompt shown to students
- `rubric` (text, NOT NULL) — hidden rubric guiding LLM feedback

**`iyow_submission` table** — IYOW submission details:

- `id` (int, PK, autoincrement)
- `submission_id` (int, FK → submission.id, unique, NOT NULL) — 1:1 with base submission
- `response_text` (text, NOT NULL) — student's written response
- `feedback` (text, nullable) — LLM-generated feedback (null until processed)
- `async_job_id` (int, FK → async_job.id, nullable) — tracks LLM processing

### 2. REST API & Model Scaffolding

Begin detailing your API in your design document by:

- Defining REST API routes that clearly support your 2x most critical user stories.
- Define the Pydantic models your feature's REST API will require.

Your document should clearly communicate:

- Route HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) and paths.
- The purpose of each route.
- Basic descriptions of the data each route will handle.

### Submission

- Continue updating your original design document.

This structured, design-forward approach will enhance both the quality and manageability of your feature, setting a strong foundation for the development cycles ahead.