---
code: RD04
title: "`git`: Fundamental Subcommands"
date: 2026-01-07
due: 2026-01-10
type:  reading
threads: ["Tools / git"]
authors: [Kris Jordan]
---

# Ch. 2 Fundamental `git` Subcommands

This is a hands-on tutorial! Follow along by running all the commands as we go. By the end, you’ll have a solid foundation of the most fundamental `git` operations.

By the end of this chapter, you’ll know what a subcommand is and have worked with several essential `git` subcommands:

- `git config`: Setting up your identity for commits and other configurations.
- `git init`: Initialize a folder as a new, empty `git` repository.
- `git add`: Staging files for your next commit.
- `git commit`: Creating a commit to record a snapshot of your project.
- `git status`: Checking the current state of your repository.
- `git log`: Viewing your project’s history.
- `git restore`: Reverting changes when something goes awry.
- `git checkout`: Pulling files, and more, from a project's history of commits.

These subcommands will form the foundation of your `git` expertise, enabling you to start every project on the right foot and build confidence as you explore deeper features. Let’s jump right in!

## Understanding `git` Subcommands

`git` is a command-line program that relies on a subcommand convention to perform specific actions to manage your repository. A subcommand is the first string argument following `git`. Each subcommand has its own purpose, many you will begin to learn in this chapter: initializing a repository (`git init`), checking the state of your repo (`git status`), or committing changes (`git commit`).

As you get familiar with `git`, you’ll find yourself using sequences of subcommands to accomplish tasks. The beauty of `git` lies in its flexibility, but that can also make it overwhelming at first. Don’t worry—`git` includes a built-in help system for you.

### Getting Help with Subcommands

If you’re ever unsure about how to use a subcommand or what options it supports, you can ask `git` for help directly from the command line. For example:

```bash
git help commit
```

This will open a manual page describing what the `commit` subcommand does, its syntax, and the available options. For example, you’ll see some descriptive, helpful text like this:

```
NAME
       git-commit - Record changes to the repository

SYNOPSIS
       git commit [-m <msg>]

DESCRIPTION
       Create a new commit containing the current contents of the index and
       the given log message describing the changes.
```

You can also use shorthand to view help inline by adding `--help` after the subcommand, like so:

```bash
git commit --help
```

This approach works for any subcommand. It’s a great way to learn as you go and explore new tools in the `git` toolbox.

### Consulting with an LLM

If you find yourself struggling to remember the exact subcommand or short flag to achieve your goal with `git`, or how to do something complex, a great use of an LLM like ChatGPT is asking it how to achieve your specific task. Describe what you want to do, ask for the `git` command(s) you need, and ask it to explain each step to you. Ultimately, you need to know _what_ `git` can do and how to think in terms of its underlying data structures and conceptual model. That's why we are putting a significant emphasis on mastering `git` in COMP423!

## Configure your name and email

Before you start using `git`, set your name and email. This information will be attached to your commits.

Run these commands in your terminal, replacing the placeholders with your details:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

These commands tell `git` who you are. The `--global` flag ensures this configuration applies to all your projects.

You can check your configuration anytime with:

```bash
git config --list
```

Sample output:

```bash
user.name=Your Name
user.email=your.email@example.com
```

This confirms your details are correctly configured. You can also see additional configuration settings. We will not worry ourselves with the depths of `git` configurability in this course.

---

## Initializing Your First Repository

### Step 1: Create a Directory

Let’s create a new directory for your project:

```bash
mkdir git-for-423
cd git-for-423
```

Here’s what these commands do:

- `mkdir git-for-423`: Creates a new directory called `git-for-423`.
- `cd git-for-423`: Changes into that directory so you can work inside it.

### Step 2: Initialize `git`

Turn this directory into a `git` repository by running:

```bash
git init
```

This creates a hidden `.git` directory, which is where all the magic happens. The `.git` directory contains:

- Your entire project history, including every commit.
- Metadata about your repository.
- Configuration files and references to other states in your project.

It’s incredible that even for massive projects with thousands of files and decades of history, this one hidden directory contains everything `git` needs to manage the project.

You can peek at it:

```bash
ls -a
```

Sample output:

```bash
.  ..  .git
```

This shows the `.git` directory alongside the regular and parent directory entries. The `.git` directory is what transforms a regular directory into a powerful `git` repository. If you peek further inside, with `ls .git`, you will see that there are more files and directories in it. The details of this structure are below the **layer of abstraction** we are focused on in learning `git`. However, note that your whole repo's history will be _right there_ and there's no magic to it, just data structures and algorithms!

---




## Making Your First Commit

### Step 1: Create a File

Let’s start by adding a README file:

```bash
echo '# Welcome to COMP423!\n' > README.md
```

This command creates a file named `README.md` with the text \`# Welcome to COMP423!\` as its content. The `>` operator redirects the text into the file. You learned about output redirection in COMP211: Systems Fundamentals.

### Step 2: Check the Repository Status

Use `git status` to see what’s happening in your repo:

```bash
git status
```

Sample output:

```bash
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	README.md

nothing added to commit but untracked files present (use "git add" to track)
```

This tells you that `README.md` is untracked, meaning it isn’t part of version control yet.

### Step 3: Stage the File

To tell `git` you want to include `README.md` in your next snapshot, stage it:

```bash
git add README.md
```

Sample output:

```bash
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   README.md
```

This confirms that `README.md` is staged and ready to commit.

### Step 4: Commit Your Changes

Create your first commit:

```bash
git commit -m "Add README file"
```

The `-m` flag specifies a commit message directly in the command.

Sample output:

```bash
[main (root-commit) abc1234] Add README file
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
```

This shows:

- The branch name (`main`) and that it's the `root-commit` where root is the first "node" in a repository.
- The unique commit hash (`abc1234`). Your hash will be different!
- A summary of changes: 1 file added with 1 line of content.

Congratulations! You’ve just recorded your first piece of project history.

---

## Adding Another Commit

Modify `README.md`:

```bash
echo "This repository is for learning git." >> README.md
```

This appends the text to `README.md`. The `>>` operator adds text to the file without overwriting it. You may recall learning about this in COMP211: Systems Fundamentals.

Check the status:

```bash
git status
```

Sample output:

```bash
On branch main

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md
```

This shows that `README.md` has been modified but not yet staged.

Stage the changes:

```bash
git add README.md
```

Commit them:

```bash
git commit -m "Update README with project purpose"
```

Sample output:

```bash
[main abc5678] Update README with project purpose
 1 file changed, 1 insertion(+)
```

Now your repository has two commits. Use `git log` to view them:

```bash
git log
```

Sample output:

```bash
commit abc5678
Author: Your Name <your.email@example.com>
Date:   Tue Jan 1 12:05:00 2025 +0000

    Update README with project purpose

commit abc1234
Author: Your Name <your.email@example.com>
Date:   Tue Jan 1 12:00:00 2025 +0000

    Add README file
```

Each commit references its parent(s), forming the **DAG** of your project history.

## How `git` Tracks File and Repo State

Here’s a diagram of how `git` tracks files:

``` mermaid
sequenceDiagram
    participant WorkingDir as Working Directory<br>(Unchanged)
    participant Changed as Working Directory<br>(Changed)
    participant Staged as Staged<br>(Index)
    participant Committed as Commit<br>(Committed History)

    WorkingDir ->> Changed: Modify File
    Changed ->> Staged: git add
    Staged ->> Committed: git commit
    Changed ->> WorkingDir: git restore <file>
    Staged ->> Changed: git restore --staged <file>
    Committed ->> WorkingDir: git checkout <commit> <file>
```

Use `git status` often to see where your files are in this flow.

## Experimenting with Commits and Changes

Now that you’ve made a few commits, let’s dive deeper into how `git` helps you manage and explore your project’s history. Follow these steps to get hands-on experience:

### 1. View Your Project’s History

Use the `git log` command to see all your commits:

```bash
git log
```

For a compact summary, try the `--oneline` option:

```bash
git log --oneline
```

This shows each commit’s hash and its message in a single line, making it easier to navigate.

!!! aside "Shortened Hashes in `git`"
    In `git`, you can refer to commits by shortened versions of their hashes. For example, instead of using the full SHA-1 hash like `abc5678abc5678abc5678abc5678abc5678abc5`, you can simply use the first few characters, like `abc5678`. This works as long as the prefix uniquely identifies a commit in the repository.

    Remember from COMP210 how hash tables rely on unique keys and the odds of collision depend on the hash function and key space? `git`'s SHA-1 hashes are 160 bits long, providing \(2^{160}\) possible values—an astronomically large number. Even with millions of commits, the probability of two full hashes colliding is practically zero.

    However, when using shortened hashes, you only need enough characters to uniquely identify a commit. For instance, using 5 hexadecimal characters gives \(16^5 = 1,048,576\) possible values. In a project like ours with only two commits so far, the chance of ambiguity is nonexistent. As your project grows, `git` will warn you if a prefix becomes ambiguous and requires more characters to ensure uniqueness.

!!! challenge "Challenge"
    Look for the hash of your first commit. You’ll use it in the next step!

---

### 2. Revisit a Previous Commit

Imagine you want to see what your project looked like at the time of your first commit.

1. Use the `git checkout` command to switch to that specific commit:
   ```bash
   git checkout <commit-hash>
   ```
   Replace `<commit-hash>` with the hash of your first commit (e.g., `abc1234`).

2. Inspect the file’s contents:
   ```bash
   cat README.md
   ```

   Notice how the content matches the snapshot from your first commit.

3. Return to the latest version of your project:
   ```bash
   git checkout main
   ```

!!! tip
    Always return to a branch (like `main`) when you’re done exploring past commits to avoid confusion.

---

### 3. Undo a File Change

Let’s say you accidentally modify a file and want to undo the changes. For example:

1. Modify the `README.md` file:
   ```bash
   echo "Oops, made a mistake!" >> README.md
   ```

2. Use `git restore` to revert the file to its previous state:
   ```bash
   git restore README.md
   ```

3. Verify the file is back to its original form:
   ```bash
   cat README.md
   ```

---

### 4. Unstage Changes

Suppose you’ve staged a file but then change your mind. Here’s how to unstage it:

1. Modify and stage the file:
   ```bash
   echo "Temporary change" >> README.md
   git add README.md
   ```

2. Unstage the file:
   ```bash
   git restore --staged README.md
   ```

Run `git status` to confirm the file is no longer staged but still modified.

---

### 5. Challenge: Explore and Restore

Use what you’ve learned to experiment:

- Inspect specific file versions from past commits using `git checkout`.
- Revert untracked or staged changes using `git restore`.
- Play around with `git log` to navigate your project history.

By combining these commands, you can confidently manage and explore your repository’s state at any point in its timeline.

---

