---
code: RD07
title: Branching and Merging
date: 2026-01-12
due: 2026-01-13
type:  reading
threads: ["Tools / git"]
authors: [Kris Jordan]
---

# Ch. 3 Branching and Merging

Imagine this: you're working on a project like a collaborative web app, and you want to test out a bold new feature—maybe integrating a third-party login system—without disrupting the stable version already in use by other team members. In software teams, branching allows experimentation like this without risk. Or maybe you're part of a team, and multiple people are working on different features at the same time. How do you keep everything organized and avoid stepping on each other's toes? That’s where **branching** and **merging** come in—two of Git’s most powerful features.

---

## What is a Branch?

In Git, a **branch** has very simple, beautiful implementation: a branch is just a **named pointer to a commit** with the special behavior that **when you create a new commit while working on a branch, the branch pointer automatically updates to reference the new commit**. No other branch pointers are updated. This implementation idea gives rise to a powerful conceptual **abstraction**: branches conceptually represent multiple parallel version histories in a repository. 

When you first create a new branch, no change in your project's history occurs; instead, a new pointer to the last commit on your current branch is created. This means the two branches start off identical, both pointing to the same commit, sharing the same history. As two individual branches have additional commits added to them independently their histories will diverge, reflecting the different paths of development taken. When you decide it is time to incorporate work on one branch back into another branch, one branch's changes can be merged into another branch.

### Why Use Branches?

Branches are incredibly useful for:

- **Experimentation**: Try out new ideas without impacting the stable version of your project.
- **Parallel Development**: Multiple team members can work on different features or fixes at the same time.
- **Code Review**: Branches allow you to submit changes for review before merging them into the main codebase.

By isolating work on separate branches, you reduce the risk of overwriting someone else’s changes or introducing bugs into your `main` branch.

### Branch Early and Often

One of the best things about Git branches is how lightweight and fast they are. Think about _why_ their implementation makes them lightweight and fast. This speed allows developers to create and switch between branches almost instantaneously, which is especially beneficial in modern workflows. For example, developers can branch off to work on features or fixes, test their changes in isolation, and merge them back quickly without delaying others’ progress. There’s virtually no cost to having as many branches as you need. This makes branches an essential tool for developers.

**Key idiom**: Branch early and often! Instead of making all your changes directly on `main` or a long-lived branch, create a branch for each new feature, bug fix, or experiment. This approach keeps your work isolated, makes it easier to collaborate, and allows for smoother integration later. Don’t hesitate—branches are free, use them liberally!

---

## What is `HEAD`? Git's *Current Working Branch*

`HEAD` is a special pointer in Git that tells you **where you are currently working** in your project’s history. When `HEAD` is "**attached**" to a branch, you can think of `HEAD` as your **current working branch**. This is analogous to how your shell maintains your current working directory (CWD) such that shell commands you run are _relative_ to your CWD. Git commands are relative to `HEAD`. 

Understanding `HEAD` helps you anticipate how Git commands behave:

- `git commit`: Creates a new commit whose parent is the commit `HEAD` currently refers to. The branch `HEAD` is attached to is updated to refer to the freshly minted commit. This is how branches stay current with their latest commit.
- `git log`: By default, displays commit history starting from `HEAD`.
- `git restore`: Reverts files to the state they were in at the commit `HEAD` resolves to, allowing you to discard unwanted changes.
- `git switch`: Causes `HEAD` to attach to a different branch and updates your working directory's contents to match the snapshot of that branch’s latest commit. If you have modified files that haven’t been staged, `git switch` will fail with a message letting you know you have uncommitted changes that are at risk of being overwritten.

!!! warning "Sometimes `HEAD` is _not_ attached to a branch."

    You will learn more about a _detached `HEAD`_ state soon. It sounds spookier than it is. It just means `HEAD` points to a specific commit rather than to a branch. As soon as you create a new branch, which you will learn how to do next, you will no longer be in a detached `HEAD` state. This is useful when you want to go back to check out a commit that no branch currently points to, but nothing to concern ourselves with now.

---

## Working with Branches

To work with branches in Git, the recommended modern commands are `git branch` and `git switch`. While `git checkout` is still available and widely used, it has a broader scope, which can make it less intuitive for branch-specific tasks. Let’s dive into best practices:

### Creating a Branch

To create a new branch, use the following command:

```bash
git branch cool-feature
```

This creates the branch but doesn’t switch you to it. **This command only creates a new pointer to the current commit that the `HEAD` branch is on.** No history has changed, and no parallel history exists yet. At this point, the two branches are exactly equivalent to each other and both point to the exact same commit.

To start working on the new branch immediately, use:

```bash
git switch cool-feature
```

Once you understand these two steps independently, you can combine them with one command:

```bash
git switch --create cool-feature
```

The `--create` flag, whose short variant is `-c`, combines creating a branch and switching to it in one command. Now, `HEAD` is pointing to `cool-feature`, and you’re ready to make changes.

### Viewing Branches

To see all the branches in your project and which one `HEAD` is pointing to:

```bash
git branch
```

For example, if you have two branches (`main` and `cool-feature`), and you are currently on the `cool-feature` branch, the output will look like this:

```plaintext
* cool-feature
  main
```

The asterisk (`*`) indicates the branch that `HEAD` is currently pointing to. Again, think of `HEAD` as your **current working branch**.

### Adding a New Commit to a Branch

Once you’re on the `cool-feature` branch and ready to make changes, you can add a new commit as follows:

(1) Modify a file in your project, for example, editing `README.md` to include some additional content.

   ```plaintext
   # Welcome to COMP423!
   This repository is for learning git.
   Branching and merging is powerful!
   ```

(2) Stage the changes using `git add`, review your staged work with `git status`:

   ```bash
   git add README.md
   git status
   ```

(3) Commit the changes with a descriptive message:

   ```bash
   git commit -m "Add a note about branching and merging"
   ```

   After committing, Git will output something like:

   ```plaintext
   [cool-feature abc1234] Add a note about branching and merging
    1 file changed, 7 insertions(+)
   ```

(4) Inspect the commit history using `git log` to see how the branch’s `HEAD` has moved forward:

   ```bash
   git log --oneline
   ```

   Example output:

   ```plaintext
   abc1234 (HEAD -> cool-feature) Add a note about branching and merging
   ```

   Here, you can see that `HEAD` has advanced to the new commit `abc1234` (your commit ID will be different) on the `cool-feature` branch.

### How `HEAD` and Branch Updates Work

When you create a commit, Git uses `HEAD` to determine the parent of the new commit. The new commit will have the commit that `HEAD` was previously pointing to as its parent. After the commit is created, Git updates the branch that `HEAD` is attached to so that it points to the new commit. This is why the branch you’re working on moves forward with each commit you make. Yes, this is the second or third time this tutorial has repeated this and for good reason: once your mental model fully internalizes this concept you will find working with branches much, much easier to understand!

### Switching Between Branches

To move between branches, whose histories are now different, use `switch` again:

```bash
git switch main
```

In practical terms, switching branches allows you to work on completely different features or bug fixes without overwriting or disrupting your current progress. For example, your `cool-feature` branch included some new text in `README.md`, switching back to `main` will revert the working directory, and therefore `README.md`, to reflect the last commit made in the `main` branch. You can then easily switch back to `cool-feature` and be back on its timeline. This separation ensures that changes in progress do not accidentally affect production or stable environments.

### Handling In-Progress Changes When Switching Branches

Sometimes, you’ll need to switch branches while you have in-progress changes in your working directory or staging. For example, you might need to review a colleague’s work or fix a bug on another branch. 

In such cases, you have three main strategies to proceed with:

#### 1. Commit Your Changes to Your Branch

If your current changes are in a good state, you can commit them to the current branch before switching:

```bash
git add .
git commit -m "WIP: Save progress on feature"
```

This ensures your work is saved and associated with the current branch. Once committed, you can switch branches without any issues:

```bash
git switch branch-name
```

!!! info "WIP is Work in Progress"

    WIP is a common acronym in the softare engineering world. It is an abbreviation for **Work in Progress**. We are all WIPs.

#### 2. Stash your Changes away Temporarily

If your changes are not ready to be committed, you can temporarily set them aside using the stash:

```bash
git stash
```

This stores your changes in a separate stash area and reverts your working directory to match the last commit. You can then switch branches:

```bash
git switch branch-name
```

When you return to your original branch, you can restore the stashed changes by "popping" them from your stash stack:

```bash
git stash pop
```

#### 3. Discard Your Changes

If the changes you’ve made aren’t needed, you can discard them using previously learned commands:

```bash
git restore --staged .
git restore .
```

These commands resets your working directory and clear your staging index to match the last commit on the branch, effectively throwing away any modifications. Once reset, you’re free to switch branches:

```bash
git switch branch-name
```

---

## Merging Branches

Once your work on a branch is complete, you’ll want to combine it with another branch (usually `main`). Merging into `main` is a best practice because it keeps the central branch stable and reflects the latest working version of your project. This aligns with workflows like trunk-based development, where small, frequent merges into a shared branch help reduce integration problems and ensure that everyone is working from a reliable codebase. This process is called **merging**.

### Fast-Forward Merge vs. Merge Commit

When merging, Git uses two main strategies:

#### Fast-Forward Merge

If the branch being merged hasn’t diverged from the target branch (e.g., no new commits were made on `main` since `cool-feature` started), Git can simply move the pointer of the target branch forward to the latest commit of the merged branch. This is called a **fast-forward merge**.

For instance, imagine a developer creates a branch for fixing a small bug and completes the fix without any changes occurring on `main` in the meantime. A fast-forward merge is efficient and keeps the history clean:

```bash
git merge cool-feature
```

After the merge, the history will look like a single line of commits, as if all the work was done directly on the target branch `main`.

#### Merge Commit

If the branches have diverged (e.g., both `main` and `cool-feature` have new commits), Git creates a **merge commit** to combine their histories. A merge commit has **two parent commits**, representing the tips of the branches being merged.

This strategy is particularly useful in larger projects where multiple developers are contributing. For example, if one developer has added a new feature while another has updated documentation on `main`, a merge commit preserves the distinct contributions:

```bash
git merge cool-feature
```

Here’s how the history looks with a merge commit:

```
*   Merge branch 'cool-feature'
|\
| * Commit on cool-feature
* | Commit on main
|/
```

To inspect a merge commit and see its parents:

```bash
git log --graph --oneline
```

Merge commits make it easier to trace where specific changes originated, which can be critical for debugging or auditing code.

### Step 1: Switch to the Target Branch

First, switch to the branch you want to merge into (e.g., `main`):

```bash
git checkout main
```

This step is crucial because Git applies merge operations to the branch that `HEAD` is currently pointing to. If you accidentally target the wrong branch, you might unintentionally merge unfinished or experimental changes into a stable branch like `main`, potentially introducing bugs or breaking the build. For example, imagine merging an in-progress feature branch into `main` during a product release—this could disrupt the deployment process and create significant headaches for the team.

### Step 2: Merge Your Feature Branch

Next, run the merge command:

```bash
git merge cool-feature
```

If there are no conflicts, Git will combine the changes, and you’re done! 🎉

---

## Handling Merge Conflicts

Sometimes, two branches modify the same part of a file, and Git doesn’t know which version to keep. For example, imagine two developers working on the same function in a file—one optimizes its performance while the other updates its documentation. When these changes are merged, Git identifies a conflict because both developers altered the same section of the file, requiring manual resolution. This is called a **merge conflict**. When this happens, Git will pause the merge and mark the conflicting sections in your files like this:

    ```plaintext
    <<<<<<< HEAD
    Code from the current branch
    =======
    Code from the branch being merged
    >>>>>>> cool-feature
    ```

To resolve the conflict:

(1) Use `git status` to see which files have conflicts. It will list the files that need attention:

   ```bash
   git status
   ```

   This is especially useful if multiple files are involved.

(2) Open each conflicting file and manually edit it to remove the conflict markers and choose the correct content.

(3) Add the resolved files:

   ```bash
   git add <file>
   ```

(4) Complete the merge with a commit:

   ```bash
   git commit -m "Resolve merge conflict"
   ```

If you decide you don’t want to proceed with the merge and want to return to the state before the merge started, you can abort the merge with:

```bash
git merge --abort
```

This will cancel the merge and reset your working directory to the state it was in before the merge began.

---

## Cleaning Up Branches

Once a branch has been merged, you can delete it to keep your repository tidy:

```bash
git branch -d cool-feature
```

If the branch hasn’t been merged but you still want to delete it, use:

```bash
git branch -D cool-feature
```

---

## Modern Git: Why use `git switch` rather than `git checkout`?

Many tutorials and older users of `git` will use `checkout` where you are learning to use `switch`. Why?

`git switch` was introduced in Git version 2.23 (August 2019) as part of an effort to make Git’s commands more user-friendly and less ambiguous. Historically, `git checkout` handled many different tasks, from switching branches to checking out individual files or commits. This multitasking nature often led to confusion for new users and even experienced developers.

By separating branch-related operations (`git switch`) from other tasks like checking out specific files or commits (`git checkout`), Git improved usability and reduced the likelihood of mistakes. 

For most branching tasks, `git switch` is the modern and preferred choice. It simplifies workflows and makes commands more intuitive for beginners and teams alike.

- **Use `git switch`** for creating or moving between branches. It’s explicit and avoids accidentally losing work or entering a detached `HEAD` state.
- **Use `git checkout`** when you need to:
    - Recover a specific file from a previous commit:
      ```bash
      git checkout <commit-hash> -- <file>
      ```
    - Temporarily view or test a specific commit without creating a new branch (a detached HEAD state):
      ```bash
      git checkout <commit-hash>
      ```
---

## Key Takeaways

* A Git branch is a lightweight pointer to a commit. Your current working branch updates to point to new commits added to the branch.
* Use branches to isolate work, experiment, and collaborate without impacting other branches.
* Create branches early and often; they’re fast, lightweight, and encourage clean workflows.
* HEAD points to your current working branch or commit and guides Git commands.
* Use git switch to create or move between branches; it’s modern and more intuitive than git checkout.
* Branches can be merged either by fast-forwarding (when no divergence) or merge commits (when histories diverge).
* Resolve merge conflicts manually by editing files, staging changes, and committing resolutions.
* Delete merged branches with git branch -d to keep your repository clean.
* Commit, stash, or discard current changes in your working directory before switching branches to avoid conflicts or lost work.

---

## Subcommands Covered

- **`git branch`**: Create, list, or delete branches; the core tool for managing branches.  
- **`git branch -d`**: Safely delete branches that have been merged. `-D` is the unsafe variant.
- **`git switch`**: Switch between branches or create and switch in one step with `--create`.  
- **`git merge`**: Combine changes from one branch into another, creating a unified history.  
- **`git merge --abort`**: Cancel a merge when there are conflicts and return to the pre-merge conflict state.
- **`git log --graph --oneline`**: Visualize commit history with branch relationships.
- **`git stash`**: Temporarily stash away changes to focus on other tasks or branches.  
- **`git stash pop`**: Recover stashed changes to the current working directory.
