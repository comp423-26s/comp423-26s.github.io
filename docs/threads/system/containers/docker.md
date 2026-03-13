---
code: LS21
title: "Container Fundamentals"
threads: ["System / Containers"]
authors: [Kris Jordan]
date: 2026-03-13
due: 2026-03-22
---

# Containers and Docker

So far in this course, you have built software that runs directly on your computer. Your Python code runs as a **process** on your operating system, reads and writes files from your filesystem, and communicates with other programs over the network.

This works well while developing locally. But modern software systems must run consistently across many environments:

* your laptop
* your teammate's computer
* automated testing servers
* production infrastructure in the cloud

Each environment may differ in operating system, installed libraries, system dependencies, and configuration.

**Containers solve this problem** by packaging software together with its runtime environment.

Docker is the most widely used container system. In this reading we examine how Docker works and how containers connect to operating system concepts you already know.

---

# Learning Objectives

After completing this reading, you will be able to:

1. Explain the difference between a **Docker image** and a **Docker container**.
2. Describe the **"one container = one primary process"** model.
3. Explain how containers provide **process isolation** using operating system features.
4. Explain how Docker runs on **Linux vs macOS vs Windows**.
5. Describe how **Docker images are built** using Dockerfiles and layered filesystems.
6. Explain how containers can mutate their filesystem and maintain **ephemeral state**.
7. Describe the role of **volumes** for persistent data.
8. Explain container **networking** between containers and the host.
9. Describe how Docker images are **immutable artifacts** distributed through registries.
10. Walk through the **lifecycle of a container**.

---

# 1. Containers as Portable Environments

Consider a simple Python web service. To run it locally you might need:

* Python 3.12
* FastAPI
* system libraries
* environment variables

If another developer has a slightly different environment, the software might behave differently.

Containers package together:

* application code
* runtime
* system dependencies
* configuration

The result is a portable runtime artifact.

Instead of describing a long setup process, we can run the system with a single command:

```
docker run my-service
```

---

# 2. Image vs Container

Docker revolves around two fundamental concepts.

## Image

A **Docker image** is a read-only template describing an execution environment.

An image contains:

* operating system filesystem layers
* installed runtime software
* application code
* configuration
* the command that should run by default

Images are **immutable**. Once built, their contents do not change.

Example image:

```
python:3.12
```

This image contains:

* a Linux base system
* Python installed
* standard libraries

## Container

A **container** is a **running instance of an image**.

If an image is a blueprint, the container is the running system.

```
docker run python:3.12
```

This command:

1. creates a container from the image
2. starts the container's primary process

Multiple containers can be created from the same image.

```
container A -> python:3.12
container B -> python:3.12
container C -> python:3.12
```

Each container runs independently.

### Mental Model

```
Image
  filesystem template

Container
  running process + writable layer
```

---

# 3. The One‑Process Container Model

A core design principle of containers is:

```
one container = one primary process
```

Examples:

* an API container runs the API server
* a database container runs the database process
* a worker container runs a background worker

When the main process exits, the container stops.

This design makes containers predictable and composable. Complex systems are built by connecting many small containers together.

---

# 4. Containers and Process Isolation

At a systems level, containers are still **ordinary processes running on the host machine**.

However they run inside isolated environments created by the Linux kernel.

Docker relies on two important kernel features.

### Namespaces

Namespaces isolate resources such as:

* process IDs
* filesystem views
* network interfaces

### Control Groups (cgroups)

Control groups limit resource usage such as:

* CPU
* memory
* IO

Inside a container, the process might appear as:

```
PID 1: uvicorn main:app
```

But the same process is still running on the host machine.

Containers therefore provide strong isolation **without requiring a full virtual machine**.

---

# 5. Why Containers Start Faster than Virtual Machines

Virtual machines run their own operating system kernel.

Containers instead **share the host kernel**.

```
Virtual Machine
  guest OS kernel
  runtime
  application

Container
  runtime
  application
```

Because containers do not boot a full operating system, they typically start in **milliseconds rather than minutes**.

---

# 6. Docker on macOS and Windows

Containers rely on Linux kernel features.

Because macOS and Windows do not use the Linux kernel, Docker runs containers inside a lightweight Linux virtual machine.

Architecture:

```
Laptop

macOS / Windows

Docker Desktop

Linux Virtual Machine

Docker Engine

Containers
```

Your `docker` command communicates with the Docker engine running inside the Linux VM.

On Linux systems, containers run directly on the host kernel.

---

# 7. The Docker Engine Architecture

Docker uses a client‑server architecture.

```
Docker CLI
   |
Docker Daemon (dockerd)
   |
Container Runtime
   |
Containers
```

The CLI sends commands to the Docker daemon, which manages images and containers.

---

# 8. Building Images with Dockerfiles

Images are constructed using a **Dockerfile**.

Example:

```Dockerfile
FROM python:3.12

WORKDIR /app

COPY pyproject.toml .

RUN pip install fastapi uvicorn

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Each instruction creates a new **layer** in the image.

### Layered Filesystem

```
Layer 4  application code
Layer 3  dependencies
Layer 2  python runtime
Layer 1  linux base
```

Docker reuses cached layers when possible.

This is why ordering Dockerfile steps carefully improves build speed.

---

# 9. Build Context

When you run:

```
docker build .
```

The `.` represents the **build context**.

Docker sends all files in this directory to the Docker daemon.

Projects often include a `.dockerignore` file to exclude:

* datasets
* build artifacts
* secrets

Reducing the build context improves build speed and security.

---

# 10. Container Filesystems and Ephemeral State

Images are read‑only, but containers can modify their filesystem.

When a container starts, Docker creates a **writable layer** above the image layers.

```
Image Layers (read‑only)
-----------------------
base OS
runtime
app code

Writable Container Layer
-----------------------
logs
runtime files
caches
```

If the container is deleted, the writable layer disappears.

This is known as **ephemeral container state**.

---

# 11. Volumes and Persistent Storage

For persistent data, Docker provides **volumes**.

Example:

```
docker run -v mydata:/var/lib/postgres postgres
```

The database writes data to the volume rather than the container layer.

Deleting the container does not delete the volume.

Volumes are essential for stateful services such as databases.

---

# 12. Container Networking

Containers have isolated networking environments.

Each container receives its own IP address.

To expose a service to the host:

```
docker run -p 8000:8000 my-api
```

This maps:

```
host:8000 -> container:8000
```

Containers inside the same Docker network can communicate using **service names as hostnames**.

---

# 13. Environment Variables and Configuration

Containerized applications often use environment variables.

Example:

```
docker run -e DATABASE_URL=postgres://... my-api
```

This allows the same image to run in different environments.

---

# 14. Logs and Observability

Containers typically write logs to **stdout and stderr**.

Docker captures these logs.

```
docker logs container_id
```

This approach works well with modern monitoring systems.

---

# 15. Image Registries and Distribution

Images are stored and shared using **registries**.

Image names follow the format:

```
registry / organization / repository : tag
```

Example:

```
docker.io/library/python:3.12
```

Images can be uploaded:

```
docker push my-org/my-api:1.0
```

And downloaded anywhere:

```
docker pull my-org/my-api:1.0
```

Images therefore behave like deployable software artifacts.

---

# 16. Container Lifecycle

Containers move through a simple lifecycle.

### Create

```
docker create my-api
```

### Start

```
docker start container_id
```

or directly:

```
docker run my-api
```

### Running

The container runs until its primary process exits.

### Stop

```
docker stop container_id
```

### Remove

```
docker rm container_id
```

Removing the container deletes its writable filesystem layer.

---

# 17. Code Activity: Exploring a Container

Run a temporary container with an interactive shell.

```
docker run -it python:3.12 bash
```

Inside the container try the following commands.

```
ls /
ps
cat /etc/os-release
```

Questions to consider:

* What operating system is inside the container?
* What process is PID 1?
* Does the filesystem look like your host machine?

This activity demonstrates that containers are **isolated runtime environments built on top of the host OS**.

---

# 18. Code Activity: Inspecting Containers

Start a container in detached mode.

```
docker run -d -p 8000:8000 python:3.12 python -m http.server
```

Now explore the container using Docker tools.

```
docker ps
```

```
docker logs <container_id>
```

```
docker exec -it <container_id> bash
```

These commands help you debug and inspect running containers.

---

# 19. Containers in Modern Systems

Modern applications are often composed of multiple containers.

Example architecture:

```
FastAPI container
Postgres container
Redis or RabbitMQ container
Worker container
```

Each container performs one role and communicates over the network.

Tools like **Docker Compose** and **Kubernetes** help orchestrate these multi‑container systems.

---

# Key Takeaways

Containers package software together with its runtime environment.

The most important ideas are:

* **Images** are immutable templates
* **Containers** are running instances of images
* Containers isolate processes using OS features
* Containers typically run **one primary process**
* Containers have ephemeral filesystems
* **Volumes** provide persistent storage
* **Port mapping** connects containers to the host
* Images are distributed through registries

Containers are now the standard unit of deployment for modern software systems.
