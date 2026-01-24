---
code: RD11
title: "Human Communication and API Design: A Shared Foundation"
date: 2026-01-23
due: 2026-01-27
type:  reading
threads: ["System / APIs"]
authors: [Kris Jordan]
---

# 3. Human Communication and API Design: A Shared Foundation

Building on the importance of communication in the software development life cycle, we now turn our attention to APIs—**Application Programming Interfaces**. Just as intentional communication strategies help teams of humans align and collaborate, APIs serve as the structured communication layer that allows different software systems to work together effectively.

## Communication as a Bridge

In both human and system communication, shared understanding is built through structured exchanges of information. Consider how people communicate:

- A **sender** conveys a message.
- A **receiver** interprets the message.
- A shared **language** or set of conventions ensures both parties understand each other.
- **Feedback** confirms whether the message was received as intended.

Now consider how client-server APIs classically function:

- A **client** (the sender) sends a request to a server.
- The **server** (the receiver) processes the request.
- Both client and server rely on shared protocols and formats, such as predefined rules for **requests** and responses, to ensure clarity. API requests typically include:
    - **"who"** the recipient is. The _who_ of an API request is typically a server address (e.g. `api.instagram.com`) and not at all "who" in the human sense.
    - **"where"** the resource is found via routing the request once it reaches the server. Typically this includes some identifying information (e.g. a _path_ like `/profiles/therealkrisjordan` or `/post/1234`).
    - **"what"** the action being requested on this resource is (verb). Is the action asking for data about resource? Creating new or updating existing resources? Deleting a resource?
    - Additional information needed to process the specific request. This information tends to be either metadata (such as what kind of format you would like in response or some identifying information of you, the sender) or data about the resource (such as a new profile bio when saving your social service profile).
- The server’s **response** serves as feedback, confirming the outcome of the interaction.
    - Status codes: did the request succeed or fail? If there was an error, what kind of error?
    - Data requested: most requests are looking for information, so the response includes the data in the format requested.
    - Metadata about the response that will be useful to the client when interpreting it.

The structure in both cases—human and system—is essential to avoiding misunderstandings and ensuring smooth collaboration.

## Analogies in Communication

To help solidify these concepts, let’s draw some direct parallels between communication in the SDLC and API design:

- **Project Specifications and API Specifications**: Just as an operating agreement or design document clarifies expectations for human collaborators, an API specification defines how systems should interact. An API can specify which operations are available, what input is required, and what kind of response to expect.

!!! info "OpenAPI Initiative"

    In the past decade, there has been a serious push toward API specification standards via the [Open API Initiative](https://www.openapis.org/what-is-openapi). We will be making use of OpenAPI standards soon in this course!

- **Language and Shared Formats**: In human communication, language provides the structure for expressing ideas. In system communication, shared formats define how data is packaged, such as using standard data encodings (e.g. JSON - JavaScript Obect Notation or XML eXtensible Markup Language) to make the information predictable and easy to interpret.

- **Feedback Loops in Teams and Systems**: Teams rely on feedback to refine their work, whether through design critiques or user testing. Similarly, APIs provide feedback through structured responses that indicate success, failure, or additional actions required.

## Empathy in API Design

Empathy is just as critical in API design as it is in human-to-human communication. In both, structure minimizes ambiguity and reduces the effort required to interpret messages. Imagine receiving a vague email like, "Please fix it ASAP," without knowing what "it" refers to or how urgent the issue really is. Similarly, an API that returns an error message like, “Something went wrong,” leaves developers guessing about what needs to be fixed.

API designers must consider the needs, constraints, and workflows of the developers who will use their APIs. This means thinking beyond technical functionality to focus on usability and developer experience. Here are some best practices when designing APIs that are a joy to use:

- **Clear Documentation**: Developers should be able to understand how to use an API without guessing. Documentation should be well-organized and provide examples that illustrate typical use cases.

- **Meaningful Feedback**: If something goes wrong, an API should return detailed and actionable messages. For instance, instead of a generic “Invalid request,” it should specify, “Missing required field: city.”

- **Consistency and Predictability**: Endpoints and request structures should follow predictable patterns, reducing the mental effort needed to learn and use the API.

- **Anticipating User Needs**: Think about common workflows or challenges developers face and design the API to simplify these tasks. For example, providing optional filters or flexible ways to retrieve data can save time and effort for users.

These practices aren't restricted to API Design, they're generally applicable principles of _human-centered design_ across many domains!

Empathy ensures that APIs are not only functional but also intuitive, reducing frustration and increasing developer productivity. When designers think about the people behind the code, and who their systems serve, they create tools that foster collaboration and innovation.