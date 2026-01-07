---
code: RD02
title: What is Source Code Management and `git`?
date: 2026-01-07
due: 2026-01-08
type:  reading
threads: ["Tools / git"]
authors: [Kris Jordan]
---

# Ch. 0 What is Source Code Management and `git`?

Imagine you're working on a group project, writing code with your friends or classmates. Things start small and simple, but as the project grows, chaos sneaks in. Who has the latest version of the code? What if two people edit the same file? What if you need to undo something from last week?

## Source Code Management (SCM)

Software development is messy. Code evolves over time, bugs are fixed, new features are added, and experiments come and go. Without a system to track these changes, you can easily lose your way or overwrite someone else’s work. Source Code Management tools offer a tried and true solution.

### A Brief History of SCM Tools

Managing project versions on a team has been a challenge since the early days of stored programs. SCM tools have been around for over 50 years that helped developers manage their projects:

- **SCSS (Source Code Control System, 1973)**: One of the earliest systems, it introduced basic source code tracking but lacked collaborative features.
- **RCS (Revision Control System, 1982):** Inspired by SCSS, a set of UNIX commands for multiple users to work on single files and track changes with diffs.
- **CVS (Concurrent Versions System, 1990):** Introduced the concept of a central repository but struggled with merging changes from multiple developers.
- **Subversion (SVN, 2000):** Improved on CVS by offering atomic commits and better branching, but still relied on a central server.
- **Distributed Systems (e.g., BitKeeper, 2000):** Allowed for more flexible workflows, without a centralized server, but was closed-source, paid software. It was a primary basis of inspiration for `git`.
- **`git` (2005):** Today's leading open source SCM was designed to handle large projects with speed, reliability, and a distributed architecture. Created by [Linus Torvalds](https://en.wikipedia.org/wiki/Linus_Torvalds) to become the Linux operating system's SCM, `git` has an [interesting origin story](https://www.linuxjournal.com/content/git-origin-story), if you're into computing history. 

## What is `git`?

`git` is a command-line tool for managing version control in projects. It allows developers to track changes in a codebase, collaborate with others, and maintain a history of project development. Unlike some tools that rely on a central server, `git` is distributed, so every user has a full copy of the project’s history on their local machine.

## What is a `git` Repository?

A `git` repository (often shortened to "repo") is a project's organized history. It stores all the information about a project, including its versions, files, branches, and more. Repositories exist locally on you and your teammates' machines, but can also be synchronized with remote repositories on the internet, via services such as GitHub.

## What is GitHub?

It’s common to hear `git` and GitHub mentioned together, often confused with one another, but it is important to recognize they’re not at all the same.

GitHub is a cloud-based platform built on top of `git`. It provides a space to host `git` repositories online, making it easier to collaborate with others by sharing your code. GitHub adds extra features for software engineering teams you will learn all about in COMP423.

While GitHub is one of the most popular platforms, it’s not the only one. Alternatives like GitLab, Bitbucket, and others offer similar functionality.

## Why Engineers Still Choose `git` 20+ Years Later

`git` is the most popular SCM today for many reasons:

1. **Distributed Workflow:** Every team member gets their own complete copy of the project's history. This means you can work offline, experiment freely, and share your work when you're ready without blocking your team mates.
2. **Fast and Lightweight:** `git` is designed to handle projects of any size efficiently, from small hobby projects to large-scale codebases. Its commands complete shockingly past compared to historical SCMs.
3. **Powerful Collaboration:** `git` enables safe collaboration with the ability review a team mate's work and incorporate thier changes when it's ready, without risking loss of your own work.
4. **Safety Net:** By keeping a history of snapshots of your project, `git` enables you to undo mistakes or recover something you deleted and later realized you needed.
5. **Open Source and Available:** `git` is free, open-source, and widely supported across different platforms.

## Installing `git` and Checking its Version

Let's be sure `git` is installed on your machine! You can check by opening a Terminal, preferably a `bash` terminal on Windows over PowerShell, and running the command `git --version`. If a reasonably modern version prints out, you're good to go! If not, continue below.

### Windows

1. Download the `git` installer from [git-scm.com](https://git-scm.com/).
2. Run the installer.
3. During setup, use the default options unless you know what you're doing. Key things to confirm:
   - **Adjusting your PATH environment**: Choose "Use `git` from the command line and also from 3rd-party software."
   - **Default editor**: Select Visual Studio Code.
4. After installation, open the Command Prompt and run:
   ```bash
   git --version
   ```
   This command checks your `git` installation by displaying the installed version number. If you see the version number, you're good to go!

   Sample output:
   ```
   git version 2.39.5
   ```
   This confirms that `git` is properly installed and ready to use. It's okay if your version is different! `git` takes pride in being highly backwards compatible, so most commands will work the same way regardless of your version.

### macOS

1. Open your terminal.
2. Run the following command:
   ```bash
   git --version
   ```
   If `git` isn’t installed, your Mac will prompt you to install the Command Line Developer Tools. Confirm the installation and follow the prompts.
3. Once installed, verify it works by running:
   ```bash
   git --version
   ```
   Sample output:
   ```
   git version 2.39.5
   ```
   This indicates that `git` is successfully installed on your macOS system. It's okay if your version is different! `git` takes pride in being highly backwards compatible, so most commands will work the same way regardless of your version.


## What to Expect Next

Now that you know *why* `git` is such a valuable tool, it’s time to learn *how* to use it. In the next chapter we’ll start using its basic commands.
