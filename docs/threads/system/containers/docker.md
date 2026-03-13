---
code: LS21
title: "Container Fundamentals"
threads: ["System / Containers"]
authors: [Kris Jordan]
date: 2026-03-13
due: 2026-03-22
---

# Container Fundamentals with Docker

By this point in the course, you have already been using containers in very practical ways. In this lesson, we will explore what containerization is in more detail so that you have a more complete picture of this important engineering infrastructure.

You installed Docker Desktop early on, have opened projects in **VS Code Dev Containers**, rebuilt those containers as your project configuration changed, added tools such as `uv` into containerized development environments, and more recently we have moved toward **Docker Compose** as projects gain more than one moving part with a relational database.

This lesson aims to answer the deeper question:

> Why are we, and so many software teams, making such significant use of containers in the first place?

Your laptop, your teammate's computer, the CI server, and a production cloud environment may all differ in operating system, installed tools, library versions, filesystem layout, and environment variables. Even small differences can lead to the classic problem of: _"it works on my machine."_

_How do we make sure software runs the same way on every machine?_ **Containers** are one of the industry's main answers to this problem. A container packages an application together with the runtime environment it expects, while still relying on the host operating system's kernel. In this course, **Docker** is the platform we use to build, run, inspect, and reason about containers.

This reading is meant to connect the hands-on container work you have already done to the systems ideas underneath it. It also foreshadows where the course is heading next: container images are not just useful for local development, they are a major building block of cloud deployment platforms such as **OKD/Kubernetes**.

## Learning Objectives

After completing this reading, you will be able to:

1. Explain the difference between a **Docker image** and a **Docker container**.
2. Describe why containers are useful for reproducible software environments.
3. Explain the **one container = one primary process** design model.
4. Describe how containers use operating system isolation features rather than a full guest OS.
5. Explain how Docker runs differently on Linux versus macOS and Windows.
6. Describe how images are built from **Dockerfiles** using **layers**.
7. Explain the difference between a container's writable layer and a **volume**.
8. Describe basic container networking, including **port publishing**.
9. Explain how images are shared through **registries**.
10. Walk through the basic **lifecycle** of a container from creation to removal.

---

## 1. Why Containers Exist

Imagine a small Python API project. To run it successfully, you may need:

- Python 3.14
- specific Python packages
- OS-level libraries
- environment variables
- a predictable working directory

Without containers, every developer and every deployment environment must recreate those assumptions manually. That is error-prone and time-consuming.

You have already seen a course-scale version of this problem. Rather than asking every student to install exactly the right Python version, tools, extensions, and CLI dependencies directly onto their host machine, the course has repeatedly leaned on Dev Containers to provide a reproducible development setup. When you rebuilt a Dev Container after changing `devcontainer.json` or a post-create script, you were already benefiting from containerization as an environment management tool.

Containers help by packaging together:

- application code
- runtime environment
- installed dependencies
- filesystem layout
- startup command

This does **not** mean a container is an entire computer or _virtual machine_. It means the container gives a process a well-defined **execution environment** so that software behaves consistently across machines.

In practice, this lets us replace a long setup checklist with a command such as:

```sh
docker run my-service
```

That command only works if an image named `my-service` already exists locally or can be pulled from a registry, but it captures the goal: a container should be easy to start and predictable to run.

In this course, the motivation for containers goes beyond local development. We also want a path from a reproducible development environment to a reproducible deployment artifact.

That progression is a big part of modern software engineering practice.

---

## 2. Image vs Container

The most important distinction in Docker is between an **image** and a **container**.

### Image

A **Docker image** is an immutable template for a runtime environment.

An image commonly includes:

- a base Linux filesystem
- installed language runtimes
- libraries and dependencies
- application source code or built artifacts
- metadata such as a default startup command

For example, `python:3.14` is the name of an image which is hosted on [Docker Hub](https://hub.docker.com/layers/library/python/3.14/images/sha256-c32bcecb0032e1ce31f9e137579cc11e4886d490eb313f847cd00b750d2283d0) that contains all of the above with a modern Python runtime version installed. This is an image. It is not yet a running process. It is a stored data file, also called an artifact, that contains the runtime environment.

### Container

A **container** is a running or stopped instance of an image.

When you run:

```sh
docker run python:3.14
```

Docker does two important things:

1. It creates a new container from the image.
2. It starts that container's configured **primary process**. Here we use the term **process* very precisely to refer to a process in the systems sense: an active, executing instance of a computer program managed by an operating system.

You can create many containers from the same image. Each container has its own process state, network identity, and writable filesystem layer. There is an analogy between a programming language's _classes_ and _instances_ and Docker _images_ and _containers_, but recognize their concerns are **very different**.

Ultimately, you will want to commit these definitions to memory:

* **Image** - immutable filesystem template + metadata
* **Container** - one instance of an image with running process state + writable storage layer

---

## 3. Containers Are Isolated Processes, Not Tiny Virtual Machines

At the operating system level, a container is still a **process** on some machine.

Docker is not primarily giving you a whole second operating system. Instead, it is giving a process an isolated environment using features of the Linux kernel. The two  important kernel mechanisms that make this possible are:

### Namespaces

Namespaces isolate what a process can see. They can provide separate views of:

- process IDs
- network interfaces
- mount points / filesystems
- hostnames
- users and groups

Inside a container, a process may believe it is running as process `1`, with its own network stack and filesystem view, even though from the host's perspective it is just one process among many.

### Control Groups (cgroups)

Control groups help limit and account for resource usage such as:

- CPU
- memory
- disk IO

This matters because containers are often used in multi-service systems where resource isolation is important.

### Why This Matters

Because containers share the host kernel, they are usually much lighter weight than full virtual machines.

Compare:

```text
Virtual Machine
  guest OS kernel
  system services
  runtime
  application

Container
  shares host kernel
  runtime
  application
```

Containers often start in seconds or less because they are starting processes, not booting an entire guest operating system.

!!! note "Containers are not magic security boundaries"
    Containers provide useful isolation, but they are not the same thing as a full hardware-virtualized machine. In industry, security depends on configuration, host hardening, least privilege, and workload design. For this course, the important takeaway is that containers isolate processes using OS features rather than a separate guest kernel.

---

## 4. One Container, One Primary Process

A very useful design rule in containerized systems is:

```text
one container = one primary process
```

In production, for example, we might run one container for the FastAPI application and another for PostgreSQL. A container’s lifecycle is tied to its main process (PID 1), so when that process exits, the container stops.

That does not mean a container is limited to a single process. The main process can spawn child processes, which is how Dev Containers support editor services, language servers, interactive shells, and application processes inside the same running container.

Following a primary process model is valuable because it keeps containers predictable, composable, easy to observe, and easy to restart.

In modern systems, instead of making one huge machine image that runs everything, we usually run multiple focused containers and let them communicate with one another.

---

## 5. Docker on Linux vs macOS vs Windows

Containers rely on Linux kernel features. That creates an interesting platform problem when your host machine runs macOS or Windows.

### On Linux

Docker can run containers directly on the host because the host is already using the Linux kernel.

### On macOS and Windows

Docker Desktop runs a lightweight **Linux virtual machine** behind the scenes. The containers run inside that Linux VM, not directly on the macOS or Windows kernel.

This means that when you type `docker ...` on macOS or Windows, the Docker CLI program is talking to a Docker engine running inside a Linux environment.

**Containers are fundamentally Linux-based**, even if your laptop is not.

---

## 6. Docker Engine: A Client-Server Model

Docker uses a tiered, client-server architecture.

```text
Docker CLI
   |
Docker daemon (dockerd)
   |
images, networks, volumes, containers
```

When you run a Docker command such as `docker ps` or `docker run`, the CLI program sends a request to the Docker daemon, and the daemon manages the actual container resources.

This architecture helps explain why the Docker CLI feels like a management tool: it is asking the Docker engine to create, start, stop, inspect, and remove container resources.

---

## 7. Building Images with Dockerfiles

Images are often built from a file named `Dockerfile`.

Here is a small example for a Python API:

```Dockerfile
FROM python:3.14

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

This example says:

1. Start from the `python:3.14` base image.
2. Copy the `uv` binaries into the image.
3. Set `/app` as the working directory.
4. Copy dependency metadata in first.
5. Install the locked project dependencies with `uv`.
6. Copy the rest of the application code. (COMP211 reminder: `.` is the current directory. The first `.` is the local working directory on host, the second `.` is win the working directory `/app` following step 3.)
7. Define the default startup command.

### Layers

Each Dockerfile instruction above contributes to the image as a **layer**. Docker can reuse previously built layers when their inputs have not changed. This is why Dockerfile ordering matters.

For example, copying `pyproject.toml` and `uv.lock` and installing dependencies **before** copying the full app source can improve rebuild speed. If only your application code changes, Docker may reuse the dependency layer from cache.

### Build Context

When you run:

```sh
docker build .
```

the `.` means: "use the current directory as the build context." Docker sends that directory's contents to the daemon so instructions like `COPY . .` can work.

Projects commonly use a `.dockerignore` file to exclude:

- Git history
- virtual environments
- test artifacts
- secrets
- large local datasets

Keeping the build context small improves speed and reduces accidental leakage of files into images.

---

## 8. Writable Layer and Ephemeral State

Images are immutable, but containers can still write files while they run.

Docker makes this possible by adding a **writable container layer** on top of the image's read-only layers. This explains a subtle but important point:

- the data of an **image** is read-only to its containers
- each **container instance** can save data changes to its **writable layer** while it is running

If you remove the container, that writable layer disappears with it.

This is why we say container state is often **ephemeral**.

For stateless services, this is fine and even desirable. For stateful services such as databases, we usually need a more durable storage mechanism.

---

## 9. Volumes for Persistent Data

To persist data independently from a container's writable layer, Docker provides **volumes**.

For example:

```sh
docker run --volume postgres-data:/var/lib/postgresql/data postgres
```

In this case, PostgreSQL stores its database files in a Docker-managed volume rather than only inside the container layer.

Volumes are valuable because:

- stopping the container does not delete the volume's data
- removing the container does not delete the volume by default
- a replacement container can mount the same volume

This separation between **compute** and **durable state** is a major systems concept.

!!! question "Check for understanding"
    If you remove a PostgreSQL container without using a volume, what happens to the database files stored only in that container's writable layer?

---

## 10. Container Networking and Port Publishing

Containers run in isolated network environments. A container can listen on a port **inside** its own network namespace without automatically exposing that port to your host machine.

To make a service reachable from your laptop, you publish a port:

```sh
docker run --publish 8000:8000 my-api
```

This maps:

```text
host port 8000 -> container port 8000
```

The left side is the host port. The right side is the container port.

This matters whenever you run a web server, database, or any other networked service in Docker. In DevContainers, you can open the Ports tab to see these mappings from container to host. This functionality is how you are able to access your FastAPI applications and `/docs` via a port from your host machine's network address (`localhost`).

### Service-to-Service Networking

Containers on the same Docker network can communicate with one another without publishing every port to the host. In multi-container applications, Docker networking lets one service talk to another using network names rather than hard-coded IP addresses. Doing this manually requires some substantial configuration. When working with multi-container projects, **Docker Compose** simplifies and handles much of this configuration for you by mapping service names to network names. We are making use of this facility in projects where we are utilizing PostgresQL containers, such as Task 07.

---

## 11. Environment Variables and Runtime Configuration

Images are designed to be reusable across environments. We often keep environment-specific configuration outside the image itself and pass it in at runtime.

For example:

```sh
docker run --env DATABASE_URL=postgresql://... my-api
```

This lets the same image run on a developer laptop, in CI, in staging, in production without rebuilding the image for every environment-specific setting. We will explore environment variables in more detail as we prepare our applications for deployment in production.

---

## 12. Registries and Image Distribution

Images are meant to be shareable artifacts.

A **registry** is a server that stores Docker images so they can be pulled onto other machines. The canonical registry is `hub.docker.com`.

Example image reference:

```text
docker.io/library/python:3.14
```

Breaking this apart:

- `docker.io` is the registry
- `library/python` is the repository
- `3.14` is the tag

Typical workflow:

```sh
docker build -t my-org/my-api:1.0 .
docker push my-org/my-api:1.0
docker pull my-org/my-api:1.0
```

This is a key reason containers are so valuable in deployment pipelines: an image can be built once, tested, published, and then run consistently in other environments.

Since images are _immutable_ and shared between containers that utilize them, Docker caches images locally so that starting new containers with the same image is very fast and does not require a large download.

---

## 13. The Lifecycle of a Container

A container typically moves through a simple lifecycle.

### Create

```sh
docker create my-api
```

Creates a container object from an image without starting it.

### Start

```sh
docker start <container>
```

Starts a previously created container.

### Run

```sh
docker run my-api
```

This is really shorthand for: create a new container and then start it.

### Stop

```sh
docker stop <container>
```

Stops the primary process and therefore stops the container.

### Remove

```sh
docker rm <container>
```

Removes the container object and its writable layer.

The image remains available unless you remove it separately.

This is another place where folks often get tripped up:

- removing a **container** is not the same as removing an **image**
- removing a container does not automatically remove a **volume**

Those are distinct Docker-managed resources.

---

## 14. Guided Activity: Explore a Running Container

This activity is worth doing. It turns the abstractions above into something concrete.

From your **host machine's terminal** run:

```sh
docker run --rm --interactive --tty python:3.14 bash
```

### What do these flags mean?

| Flag | Purpose |
| ---- | ------- |
| `--rm` | Remove the container automatically when it exits |
| `--interactive` / `-i` | Keep standard input open |
| `--tty` / `-t` | Allocate a terminal |
| `python:3.14` | Image to run |
| `bash` | Command to run as the container's primary process |

Once you are inside the container, try:

```sh
pwd
ls /
cat /etc/os-release
ps -ef
python --version
```

Questions to think through:

1. What operating system distribution does the container appear to be using?
2. What process is running as PID `1` inside the container?
3. Does the filesystem look identical to your host machine?
4. Why does `python --version` work even if your host machine might not have that exact Python version installed?

Exit the shell with:

```sh
exit
```

Because you used `--rm`, Docker cleans up the container automatically after exit.

---

## 15. Guided Activity: Run a Background Service in a Container

Now let's run a container in the background and inspect it from the outside.

From your **host machine's terminal** run:

```sh
docker run \
  --detach \
  --name simple-http \
  --publish 8000:8000 \
  python:3.14 \
  python -m http.server 8000
```

After doing so, try opening up `localhost:8000` in your web browser. If you receive a port conflict error, check docker and be sure you do not have other containers running concurrently.

### What is happening here?

| Part | Purpose |
| ---- | ------- |
| `--detach` | Run in the background |
| `--name simple-http` | Give the container an easy name |
| `--publish 8000:8000` | Expose the service to your host on port 8000 |
| `python:3.14` | Use the Python image |
| `python -m http.server 8000` | Run a simple web server as the primary process |

Now inspect it:

```sh
docker ps
docker logs simple-http
docker exec --interactive --tty simple-http bash
```

Inside the running container, try:

```sh
ps -ef
ss -lnt
```

Then exit the shell and clean up:

```sh
docker stop simple-http
docker rm simple-http
```

Questions:

1. Why does the container stop when the `python -m http.server` process stops?
2. What would happen if you omitted `--publish 8000:8000`?
3. Why is `docker exec ... bash` different from `docker run ... bash`?

---

## 16. Containers in Real Systems

In modern software systems, it is common to split responsibilities across multiple containers.

For example:

- API container
- PostgreSQL container
- background worker container

Each container has a focused role. They communicate over a network. This makes systems easier to scale, update, replace, and reason about.

As systems grow, tools such as Docker Compose and Kubernetes help define, run, and orchestrate multiple containers together.

You are already seeing the beginning of this progression in the course:

- **Dev Containers** package development environments.
- **Dockerfiles** package applications as deployable images.
- **Docker Compose** helps manage local multi-container systems such as an API plus a database.
- **OKD/Kubernetes** runs and orchestrates containers in a cloud environment.

When you deploy to OKD/Kubernetes soon, you will not be shipping your laptop or your VS Code setup to the cloud. You will be shipping a container image and asking the platform to run it for you, connect it to networking, restart it when needed, and manage it as part of a larger system.

You do not need to master orchestration yet. The key first step is understanding what a single container is and what problem it solves.

---

## Key Takeaways

- An **image** is an immutable template; a **container** is an instance of that template.
- Containers are isolated **process environments**, not full guest operating systems.
- Containers usually follow a **one primary process** model.
- Images are built from **Dockerfiles** and optimized through **layers**.
- A container's writable layer is usually **ephemeral**.
- **Volumes** store data that must outlive a container.
- **Port publishing** connects container services to the host.
- **Registries** let teams distribute images as reusable deployment artifacts.

If you leave this reading with one strong mental model, let it be this: **Docker is a tool for packaging and running processes inside predictable, isolated Linux-based environments.**
