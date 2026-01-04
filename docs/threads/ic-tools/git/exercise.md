# Collaborating with `git` on a `MkDocs` Project

In this tutorial, you will work to create 

## How do collaborative apps address "Who can do what?"

Think about how you engage with your favorite apps daily. When you post pictures on Instagram, you control who sees them—perhaps just your close friends or maybe everyone. When collaborating on a Google Docs project, you decide whether classmates can edit or just comment. And within your Google Drive, some folders might be shared with your study group, while others remain private. These everyday interactions with social media and collaboration tools are your practical introduction to three pivotal software engineering concepts: authentication, authorization, and access control.

As you dive into building your software projects or integrate into development teams, you will encounter these patterns repeatedly. Whether crafting a straightforward web application or developing complex enterprise software, pivotal questions arise: "How do users prove who they are?", "What permissions should different users have?", and "How are these permissions enforced consistently?" Fortunately, the answers to these questions are built on established terminology and conceptual frameworks developed over many decades of software engineering projects.

### Authentication

**Authentication** is the process of verifying the identity of a user, system, or entity attempting to access a resource. This verification process involves validating one or more authentication factors, which typically fall into three categories:

* Something you know (like passwords or PINs)
* Something you have (like security tokens or smart cards)
* Something you are (like fingerprints or facial features)

The authentication process generates a digital identity that the system can then use for subsequent interactions. For example, when you log into a system, an authentication process may create a session token that represents your verified identity.

### Authorization and Access Control

**Authorization** is the process of determining whether an _authenticated identity_ has permission to perform specific actions or access particular resources. Authorization defines what an authenticated user can do within a system by evaluating their privileges against a set of rules or policies. Authorization always occurs after authentication - a system must know who you are before it can determine what you're allowed to do.

**Access Control** is the implementation mechanism that enforces _authorization decisions_ and protects resources from unauthorized access. While authorization defines the rules about who can do what, access control provides the technical mechanisms to enforce these rules. Access control systems implement various models such as:

* Role-Based Access Control (RBAC): Groups permissions into roles and assigns users to appropriate roles
* Attribute-Based Access Control (ABAC): Makes access decisions based on attributes of users, resources, and context
* Mandatory Access Control (MAC): Enforces system-wide policies that users cannot modify
* Discretionary Access Control (DAC): Allows resource owners to control access to their resources

The Relationship Chain
These three concepts work together in a sequential chain:

Authentication verifies identity ("Who are you?")
Authorization determines permissions ("What are you allowed to do?")
Access Control enforces those permissions ("Here's how we'll make sure you only do what you're allowed to do")

For example, when you attempt to access a secure file:

1. The system first authenticates you by validating your login credentials
2. Once authenticated, the authorization system checks your permissions to determine if you should have access to take an action on a given resource
3. If authorized, the access control mechanism enforces this decision by actually allowing or blocking the file access attempt