# Starting a Static Website Project with MkDocs

Welcome! In this tutorial, you'll learn how to build a static website to organize your course notes using GitHub Pages and the powerful static site generator, Material for MkDocs. By the end of this guide, you'll have a fully functional website hosted online, starting from a blank repository. Along the way, you'll also set up a basic Python development container (dev container) in Visual Studio Code (VS Code) and configure GitHub Actions for continuous integration and deployment (CI/CD) and learn what all of this useful _jargon_ means.

!!! info "Why Material for MkDocs?"

    MkDocs is the de facto documentation site generator for today's most popular, modern Python projects, including a few we'll in this course: [FastAPI](https://fastapi.tiangolo.com/) and [Pydantic](https://docs.pydantic.dev/latest/). Those sites are made and maintained with this documentation tool. Material for MkDocs is one of the most popular themes for MkDocs, offering a sleek design, responsive layout, and tons of features out of the box. As an added endorsement, I, Kris, claim this is the best and easiest to use, static site generator tool I've ever seen. In fact, **this course site you're reading right now** is [built using MkDocs](https://github.com/comp423-26s/comp423-26s.github.io/), too! (There's a recursion joke somewhere in here.)

## Why This Matters

Static websites are an essential part of software engineering and open-source projects. Many teams and individuals use them to document software, share knowledge, and create personal portfolios. Learning to build and manage one not only enhances your technical skillset but also sets you up for creating your own portfolio and blogging website.

### What You Will Learn

By completing this tutorial, you will:

- Set up a basic Python Development Container in VS Code to streamline development.
- Initialize and configure a GitHub repository for a static site.
- Use Material for MkDocs to generate a clean, professional website.
- Deploy your site to GitHub Pages with GitHub Actions for CI/CD.
- Gain insight into the tools and practices used in open-source and professional software projects.

## Prerequisites

Before we dive in, make sure you have:

1. **A GitHub account:** If you don’t have one yet, sign up at [GitHub](https://github.com).
2. **Git installed:** [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) if you don’t already have it.
3. **Visual Studio Code (VS Code):** Download and install it from [here](https://code.visualstudio.com/).
4. **Docker installed:** Required to run the dev container. [Get Docker here](https://www.docker.com/products/docker-desktop).
5. **Command-line basics:** Your COMP211 command-line knowledge will serve you well here. If in doubt, review the Learn a CLI text!

## Part 1. Project Setup: Creating the Repository

### Step 1. Create a Local Directory and Initialize Git

(A) Open your terminal or command prompt.

(B) Create a new directory for your project. (Note: Of course, if you'd like to organize this tutorial somewhere else on your machine, go ahead and change into that parent directory first. By default this will be in your user's home directory.):

   ```bash
   mkdir comp423-course-notes
   cd comp423-course-notes
   ```

(C) Initialize a new Git repository:

```bash
git init
```

!!! question "What is the effect of running the `init` subcommand?"
    
    You should know what happens when you run this command at this point in the course! If you do not, please refer back to the chapter on [Fundamental git Subcommands](../../resources/git/ch2-git-fundamental-subcommands.md).  

(D) Create a README file:

   ```bash
   echo "# COMP423 Course Notes" > README.md
   git add README.md
   git commit -m "Initial commit with README"
   ```

### Step 2. Create a Remote Repository on GitHub

(1) Log in to your GitHub account and navigate to the [Create a New Repository](https://github.com/new) page.

(2) Fill in the details as follows:

- **Repository Name:** `comp423-course-notes`
- **Description:** "Course notes organized as a static website using Material for MkDocs."
- **Visibility:** Public

(3) Do not initialize the repository with a README, .gitignore, or license.

(4) Click **Create Repository**.

### Step 3. Link your Local Repository to GitHub

(1) Add the GitHub repository as a remote:

   ```bash
   git remote add origin https://github.com/<your-username>/comp423-course-notes.git
   ```

   Replace `<your-username>` with your GitHub username.

(2) Check your default branch name with the subcommand `git branch`. If it's not `main`, rename it to `main` with the following command: `git branch -M main`. Old versions of `git` choose the name `master` for the primary branch, but these days `main` is the standard primary branch name.

(3) Push your local commits to the GitHub repository:

   ```bash
   git push --set-upstream origin main
   ```

!!! info "Understanding the --set-upstream Flag"

    - `git push --set-upstream origin main`: This command pushes the main branch to the remote repository origin. The `--set-upstream` flag sets up the main branch to track the remote branch, meaning future pushes and pulls can be done without specifying the branch name and just writing `git push origin` when working on your local `main` branch. This long flag has a corresponding `-u` short flag.

(4) Back in your web browser, refresh your GitHub repository to see that the same commit you made locally has now been _pushed_ to remote. You can use `git log` locally to see the commit ID and message which should match the ID of the most recent commit on GitHub. This is the result of pushing your changes to your remote repository.

## Part 2. Setting Up the Development Environment

### What is a Development (Dev) Container?

A dev container ensures that your development environment is consistent and works across different machines. At its core, a dev container is a preconfigured environment defined by a set of files, typically leveraging Docker to create isolated, consistent setups for development. Think of it as a "mini computer" inside your computer that includes everything you need to work on a specific project—like the right programming language, tools, libraries, and dependencies.

Why is this valuable? In the technology industry, teams often work on complex projects that require a specific set of tools and dependencies to function correctly. Without a dev container, each developer must manually set up their environment, leading to errors, wasted time, and inconsistencies. With a dev container, everyone works in an identical environment, reducing bugs caused by "it works on my machine" issues. It also simplifies onboarding new team members since they can start coding with just a few steps.

### How are software project dependencies managed?

To effectively manage **software dependencies**, it's important to understand package and dependency management. In most software projects, you rely on *external libraries or packages* to save time and leverage work that has already been done by others. Managing these dependencies ensures that your project has access to the correct versions of these libraries, avoiding compatibility issues.

In this project, our primary dependency is `mkdocs-material`, which enables us to build and style our static site. This package is available on [PyPi](https://pypi.org/project/mkdocs-material/), the Python Package Index, which is a repository of software for the Python programming language. PyPi hosts thousands of free, open source, third-party libraries that developers can use to add functionality to their projects. These libraries are installed using `pip`, a package manager for Python. Similar tools and repositories exist for other programming languages—like `npm` for JavaScript, `cargo` for Rust, or `maven` for Java.

To ensure your dependencies are always correctly installed and available, in standard Python projects relying on `pip`, requirements are traditionally listed out in a `requirements.txt` file in the project's root directory. This file is committed to your project's version control history so that as your project adds or updates dependencies, it is reflected in the project's history. This allows anyone working on the project to quickly set up their environment by installing the necessary dependencies with the `pip install` command. The dev container configuration you setup will automatically install dependencies from `requirements.txt` when the container is created. This allows anyone working on the project to have a complete environment setup in one step: starting a dev container.

In summary, the the `devcontainer.json` file specifies configuration for a consistent development environment using a Docker image. The `requirements.txt` file ensures all needed Python package for our project are installed when the container is created. Together, these files automate the process of setting up a developer environment, making it easier for you and others to work on the project. 

Lets establish your static website development environment:

### Step 1. Add Development Container Configuration

1. In VS Code, open the `comp423-course-notes` directory. You can do this via: File > Open Folder.
2. Install the **Dev Containers** extension for VS Code.
3. Create a `.devcontainer` directory in the root of your project with the following file inside of this "hidden" configuration directory:

**`.devcontainer/devcontainer.json`**

The `devcontainer.json` file defines the configuration for your development environment. Here, we're specifying the following:

- **`name`**: A descriptive name for your dev container.
- **`image`**: The Docker image to use, in this case, the latest version of a Python environment. [Microsoft maintains a collection of base images for many programming language environments](https://hub.docker.com/r/microsoft/vscode-devcontainers), but you can also create your own!
- **`customizations`**: Adds useful configurations to VS Code, like installing the Python extension. When you search for VSCode extensions on the marketplace, you will find the string identifier of each extension in its sidebar. Adding extensions here ensures other developers on your project have them installed in their dev containers automatically.
- **`postCreateCommand`**: A command to run after the container is created. In our case, it will use `pip` to install the dependencies listed in `requirements.txt`.

```json
{
  "name": "COMP423 Course Notes",
  "image": "mcr.microsoft.com/devcontainers/python:latest",
  "customizations": {
    "vscode": {
      "settings": {},
      "extensions": ["ms-python.python"]
    }
  },
  "postCreateCommand": "pip install -r requirements.txt"
}
```

### Step 2. Add `requirements.txt` Python Dependency Configuration

**`requirements.txt`**

The `requirements.txt` file lists the Python dependencies needed for the project. It should be in your project's root directory. Here, you only need to include `mkdocs-material` pinned to a specific minor version its current release:

~~~
mkdocs-material~=9.5
~~~

Pinning a dependency to a minor version ensures that the project will use the latest fixes, called patch releases, within that version. For example, `~=9.5` allows automatic upgrades from `9.5.49` to `9.5.50`, but prevents upgrades to `9.6` or beyond, ensuring stability while still benefiting from bug fixes and minor improvements. In larger software projects, this practice is valuable for maintaining a stable and reproducible development environment.

### Step 3. Reopen the Project in a VSCode Dev Container

Reopen the project in the container by pressing `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac), typing "Dev Containers: Reopen in Container," and selecting the option. This may take a few minutes while the image is downloaded and the requirements are installed.

Once your dev container setup completes, close the current terminal tab (trash can), open a new terminal pane within VSCode, and try running `python --version` to see your dev container is running a recent version of Python without much effort! (As of this writing: 3.13 released in October of 2024.)

## Part 3. Creating the Static Site with Material for MkDocs

### Step 1. Initialize MkDocs

Run the following commands in your terminal (inside the container):

```bash
mkdocs new .
```

This command works because `mkdocs` is installed in the container as part of the `requirements.txt` setup in the previous section. The `mkdocs` subcommand creates the basic file structure for your site, including a default `mkdocs.yml` configuration file and a `docs` folder.

!!! question "What is the `.` in that command?"

    You should recall this from COMP211! It refers to the current working directory the terminal's shell process is in.

The official documentation for creating a new site, which goes into more depth than this tutorial, can be found in the [official documenation for Material for MkDocs](https://squidfunk.github.io/mkdocs-material/creating-your-site/), if you are interested in additional coverage.

### Step 2. Configure Your Site

The `mkdocs.yml` file is a YAML configuration file. YAML stands for "Yet Another Markup Language" and is commonly used in software projects for configuration due to its simplicity and human-readable format. Unlike JSON, which was used in the `.devcontainer.json` file, YAML doesn’t require brackets or quotes for every element, making it cleaner and easier to read for large configurations. While JSON is more rigid and structured, YAML's flexibility and readability make it popular for configuration files, especially in tools like MkDocs, and cloud deployment tools you will soon learn about, such as GitHub Actions and Kubernetes.

Edit `mkdocs.yml` to look like this:

```yaml
site_name: COMP423 Course Notes
theme:
  name: material
```

Edit the `index.md` markdown file in the `docs` directory:

**`docs/index.md`**

```markdown
# Welcome to Your Name's Course Notes

This is my home page. I will use it to organize and share my course notes.
```

Of course, substitute your name in the title.

Markdown is a lightweight markup language that allows you to format text using simple, readable syntax. Files written in Markdown typically use the .md extension. It’s widely used in the software industry for documentation, readme files, blogs, and more due to its simplicity and flexibility.

In a MkDocs project, all your pages will be written in Markdown and then processed by MkDocs to generate HTML files for your website. This means you can write plain text and use Markdown’s syntax for headings, lists, links, and more, without dealing directly with HTML.

Here are some key benefits of Markdown:

* It’s easy to read and write.
* It works well with version control systems like Git.
* It’s supported by many platforms, including GitHub, where Markdown is used for README files.

To learn more about Markdown, check out [this comprehensive guide](https://www.markdownguide.org/).

### Step 3. Preview Your Site Locally

Run the following command to start a local development server:

```bash
mkdocs serve
```

The `serve` subcommand launches a local development web server that monitors your files for changes. This means if you edit any of the files, the server will automatically refresh the page in your browser to reflect those changes. 

Open your browser and navigate to `http://127.0.0.1:8000` to see your site. Woo! You should see the contents of your `docs/index.md` file rendered in beautiful HTML.

!!! info "What is `127.0.0.1`?"

    `127.0.0.1` is the "loopback" address, meaning it always refers to your own computer. This address is commonly used for testing web applications locally. It also means that you cannot share your local development work directly (without others without using some additional tricks beyond our concerns right now). In the next section, you will learn how to deploy a production grade version of this site live on the web.

To stop the server, return to your terminal and press `Ctrl+C`. This will terminate the `mkdocs serve` process.

## Part 4. Deploying with GitHub Pages

In this section, you will set up an automated deployment process using GitHub Actions, a tool for Continuous Integration and Continuous Deployment (CI/CD). Setting up CI/CD for your project means that every time you make changes and push them to GitHub, a series of automated steps will run to "test", build, and deploy your website. This ensures your site is always up-to-date with the latest changes you make.

Here’s what you're about to do to configure this repository's CI/CD pipeline:

1. **Add a GitHub Actions Workflow**: You'll create a workflow file that defines the automated steps for building and deploying your site on GitHub.
2. **Push Changes and Test the Workflow**: Once everything is set up, you'll push your changes to GitHub and observe the deployment process in action.

### Setting up a GitHub Action for CI/CD

#### Step 1. Add a GitHub Action for CI/CD

Create a `.github/workflows/ci.yml` file in your repository. You can do this from a Terminal in your dev container with the commands:

```bash
mkdir -p .github/workflows
code .github/workflows/ci.yml
```

This file defines the steps for the CI/CD workflow.

**`.github/workflows/ci.yml`**

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Build and Deploy
        run: mkdocs gh-deploy --force
```

- **`on.push.branches`**: Specifies that this workflow should run whenever changes are pushed to the `main` branch.
- **`permisisons.contents`**: Specifies the GitHub Action will be able to write back to this repository, needed to update the `gh-pages` branch the static site content will generate to.
- **`steps`**: These define the tasks to perform, such as checking out the code, setting up Python, installing dependencies, building the site, and deploying it. The details of GitHub action configuration are beyond our scope, but you can find the [full GitHub Action documentation here](https://docs.github.com/en/actions/writing-workflows/quickstart).

!!! note "What does the step running `mkdocs gh-deploy --force` do?"

    The `mkdocs gh-deploy --force` command builds your site into static files and pushes them to the `gh-pages` branch of your repository. This is a subcomand built into `mkdocs`. The `--force` flag ensures that any existing content in the `gh-pages` branch is overwritten, guaranteeing that the latest version of your site is deployed.

#### Step 2. Push Changes and Deploy

Now that your configuration is ready, let’s test it out:

(1) Add and commit your changes:

   ```bash
   git add .
   git commit -m "Set up Material for MkDocs and GitHub Action"
   ```

(2) Push the changes to GitHub:

   ```bash
   git push origin main
   ```

(3) Navigate to the **Actions** tab in your GitHub repository to watch the workflow run. You’ll see each step execute, and once the process completes, your site will be deployed to GitHub Pages.

(4) After the GitHub Action completes, navigate to the `gh-pages` branch in your GitHub repository to view the deployed static files. These files represent your website as hosted by GitHub Pages.

(5) To ensure your repository's Github Site is served from the `gh-pages` branch, go to your repository's **Settings > Pages**, and select the `gh-pages` branch as the source for your GitHub Pages site. Once set, your site will soon be live at the URL below.

(6) Visit your site at `https://<your-username>.github.io/comp423-course-notes` to see the changes live. Sometimes this can take a minute to update.

Congratulations! You’ve automated your deployment process with CI/CD. Now, every time you push to `main`, or merge Pull Requests into `main`, these steps will automatically be carried out resulting in your static website being regenerated and deployed. This "push-to-deploy"/"merge-to-deploy" git workflow is common in many industrial settings.

### Understanding your CI/CD Workflow

Now that your deployment is automated, let’s break down what happen step by step when you make changes to this project in the future:

1. **Commit Changes Locally:** You edit your site’s files and save your changes in your local Git repository by creating a commit.

2. **Push to GitHub:** When you push your changes to the `main` branch on GitHub, the CI/CD pipeline is triggered automatically.

3. **GitHub Action Starts:** GitHub detects the new commit and starts running the workflow you defined in `.github/workflows/ci.yml`.

4. **Workflow Steps Execute:**

    - The repository code is checked out to the runner environment.
    - A Python environment is set up, and the dependencies listed in `requirements.txt` are installed.
    - MkDocs builds the static site, converting your Markdown files into an HTML website.
    - The `mkdocs gh-deploy` command deploys the site to the `gh-pages` branch.

5. **Site is Updated:** Once the workflow completes, your GitHub Pages site automatically reflects the latest changes.

### Why This Matters Beyond This Tutorial

CI/CD is not just for static sites—it’s a critical practice in modern software development. It ensures your code is tested, built, and delivered efficiently and consistently. This approach reduces manual work, catches errors early, and speeds up development.

For example:

- In large software projects, CI/CD pipelines run tests on every commit to ensure code quality.
- For applications, pipelines can build and deploy to staging or production environments automatically.

By setting up this workflow, you’ve taken a first step toward understanding these industry-standard practices and how automation can enhance the reliability of your projects.

## Conclusion

Congratulations! You’ve successfully created a static website for your course notes using Material for MkDocs, configured a development environment, and set up automated deployment. This foundational skill can be applied to many open-source and professional projects. 

In the first exercise, you will expand your site with more pages and customizations!