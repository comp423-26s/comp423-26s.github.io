# 4. Key Concepts in HTTP

Have you ever wondered how your favorite apps communicate with servers behind the scenes? When you leave a comment on Instagram, how does the server know which post you’re commenting on and what you wrote? In this section, we'll explore how modern software systems communicate via HTTP (Hypertext Transfer Protocol), focusing on APIs (Application Programming Interfaces) and the structure that makes it all work.

## Key Terms

Understanding these concepts forms the foundation of all API interactions, whether you're building a simple weather app or a complex social media platform.

1. **Sender** (The Client): This is who initiates the communication - like your mobile app or web browser. The client is responsible for:

    - Formatting requests correctly
    - Managing user interactions
    - Handling responses appropriately
    - Retrying failed requests when necessary

2. **Receiver** (The Server): This processes the request and sends back information. The server’s responsibilities include:

    - Validating incoming requests
    - Processing data and managing resources
    - Ensuring security
    - Providing appropriate responses

3. **Medium** (The Channel): How the message travels - in modern APIs, this is typically HTTP. The medium:

    - Ensures reliable delivery of messages
    - Handles connection management

4. **Message** (The Request/Response): The actual information being exchanged. Messages must be properly formatted and complete with all necessary information.

5. **Feedback** (The Server’s Response): Confirmation that the message was received and processed. Good feedback:

    - Confirms success or failure
    - Provides helpful error messages
    - Returns requested data
    - Includes relevant metadata

A common, helpful analogy for APIs at a conceptual level is to think of it like ordering food at a restaurant:

- You (the sender/client) place an order.
- The waiter (the medium) carries the message back to the kitchen.
- Your order (the message) contains what you want.
- The kitchen (the receiver/server) processes it.
- The waiter (the medium) carries the food from the kitchen to you.
- The food arriving (the feedback) confirms your order was received and accurately processed.

## HTTP: The Medium of Modern APIs

HTTP provides a standardized way for clients and servers to talk to each other. Understanding HTTP important for any software engineer working with web or mobile applications.

### Resources: The Nouns of HTTP

In HTTP, everything is a resource - think of these as the "things" your API can interact with. Resources are fundamental to REST (Representational State Transfer), the most common architectural style for modern APIs.

Examples of resources:

- A user profile
- A social media post
- A collection of photos
- A comment thread

Each resource has its own URL (Uniform Resource Locator). URLs are technically opaque strings, but in real-world applications tend to be structured hierarchically, inspired by directory path strings, like:

```
https://api.instagram.com/users/123/posts/456/comments
```

Breaking down this URL:

- `https://`: This is the protocol of the connection (cryptographically secure HTTP)
- `api.instagram.com`: This is the domain that addresses "who" the request is sent to.
- `users/123`: Identifies a specific user.
- `posts/456`: A specific post by that user.
- `comments`: The collection of comments on that post.

### HTTP Methods: The Verbs

HTTP methods define **what** action you want to perform on a resource. Understanding each method’s purpose and proper use is valuable:

| HTTP Method | Safety   | Idempotency        | Description                                                                                              |
| ----------- | -------- | ------------------ | -------------------------------------------------------------------------------------------------------- |
| GET         | Safe     | Idempotent         | Fetches information without modifying any resources on the server                                        |
| POST        | Not Safe | **Not Idempotent** | Creates new resources on the server, with each identical request potentially creating multiple resources |
| PUT         | Not Safe | Idempotent         | Completely replaces an existing resource, with repeated identical requests having the same effect        |
| PATCH       | Not Safe | Idempotent         | Partially modifies an existing resource, only updating specified fields                                  |
| DELETE      | Not Safe | Idempotent         | Removes a resource from the server, with repeated identical requests having the same effect              |

Safety in web APIs is like reading a book versus writing in it. When a method is "safe," it means it only reads or looks at data without changing anything on the server - like how reading a book doesn't change its contents. GET is the only safe method since it just retrieves information, while methods like POST, PUT, PATCH, and DELETE are not safe because they modify data on the server, just like how writing in a book changes its contents.

Idempotency is about whether doing something multiple times has the same effect as doing it once. It's a really important property in many system designs. Think of it like pressing the button at a crosswalk: the second or third time you push it before the lights change has no additional effect (as much as we wish it sped the process up!). Similarly, saving a file many times in a row in your editor does not create multiple files. Importantly, for well implemented checkout systems, pressing "Complete Purchase" many times does not result in duplicate orders going through. These operations are idempotent. GET, PUT, PATCH, and DELETE are idempotent because repeating the same request gives you the same result, while POST is not idempotent because each request creates something new - like how pressing "send" multiple times on an email might send multiple copies of the same message.

#### GET
* Examples:
    * Viewing a user's profile page
    * Retrieving a list of blog posts
    * Fetching search results
* Common Use Cases:
    * Search operations
    * Data retrieval
    * Reading resources
    * Querying system status

#### POST
* Examples:
    * Adding a new comment to a blog post
    * Creating a new user account
    * Uploading a file to a server
* Common Use Cases:
    * Form submissions
    * File uploads
    * Resource creation
    * Data processing

#### PUT
* Examples:
    * Updating an entire user profile
    * Replacing a document with a new version
    * Setting a complete configuration
* Common Use Cases:
    * Full resource updates
    * Complete replacements
    * Configuration updates
    * Version management

#### PATCH
* Examples:
    * Updating just a user's email address
    * Modifying specific fields in a document
    * Updating part of a configuration
* Common Use Cases:
    * Partial updates
    * Field-specific modifications
    * Resource property adjustments
    * Incremental changes

#### DELETE
* Examples:
    * Removing a comment from a post
    * Deleting a user account
    * Removing a file from storage
* Common Use Cases:
    * Resource removal
    * Cleanup operations
    * Account deletion
    * Content management

## Anatomy of API Communication

Let’s mock up the big ideas of what happens when you comment on a post on Instagram.

### The Request (Client → Server)

```http
POST https://api.instagram.com/posts/12345/comments
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
    "comment": "Great photo!",
    "timestamp": "2024-01-26T10:30:00Z",
    "source": "mobile_app"
}
```

This is a simple example of the textual "envelope" of an HTTP request contains and what is transmitted over the network from client to server.

- **Method and URL**: The POST method indicates we’re creating a new comment. The URL specifies exactly which resource (the post) we’re interacting with.

- **Headers**: Headers provide essential metadata. Examples:
    - `Content-Type`: Tells the server what format the data is in.
    - `Authorization`: Proves who you are (usually a token).

- **Body**: Contains additional data about the request. In this case, it includes the comment text, the source of the action, and a timestamp.

### The Response (Server → Client)

```http
HTTP/1.1 201 Created
Content-Type: application/json
Cache-Control: no-cache

{
    "success": true,
    "message": "Comment added successfully",
    "comment_id": 789,
    "timestamp": "2024-01-26T10:30:01Z"
}
```

Key components explained:

- **Status Line**: Indicates the HTTP version, status code (201 Created), and a brief status message. We will look at status codes in more depth shortly.

- **Headers**: Includes metadata about the response. Examples:
    - `Content-Type`: Format of the response (JSON).
    - `Cache-Control`: Instructions for how clients should cache the response (or not!)

- **Body**: Contains the actual response data, confirming the action was successful and providing additional context (e.g., the new comment ID).

### Request Response Sequence Diagram

The above request, response flow can be visualized as follows:

~~~mermaid
sequenceDiagram
    participant App as Instagram App (Client)
    participant Server as Instagram Server

    Note over App: User Leaves a Comment
    App->>Server: POST /posts/12345/comments
    Note over Server: Comment Saved Successfully
    Server-->>App: 201 Created (Success!)
    Note over App: Comment Shows as Saved 
~~~

This diagram shows:

1. The client sending the comment to the server.
1. The server processing the comment.
1. A success response being returned to the client.

## Status Codes Convey Server's Handling of Request

When the server sends a response, the response starts with a status code. You've seen these in the wild: `404 Not Found` or `500 Internal Server Error`. There is an intention design to these "century" numberings. Responses within each 100-level range share something in common.

- **Informational (1xx)**: These are rarely used by API developers and are more for lower-level connection handling.
    - 101 Switching Protocols: Used when an HTTP connection is upgraded to a WebSocket connection.

- **Success (2xx)**: Indicates that the request was successfully processed by the server.
    - 200 OK: Request succeeded.
    - 201 Created: Resource was created successfully.

- **Redirection (3xx)**: Indicates the client needs to take additional action to complete their request.
    - 301 Moved Permanently: The resource has permanently moved to a new URL.
    - 302 Found: The resource is temporarily at a different URL.
    - 307 Temporary Redirect: Like 302, but the request method must not change.

- **Client Errors (4xx)**: Indicates there is something wrong with what the client sending the request is requesting.
    - 400 Bad Request: Invalid syntax or parameters.
    - 401 Unauthorized: The request could not be authenticated to a user or the user no longer exists.
    - 403 Forbidden: The user making the request does not have permission to perform the requested action.
    - 404 Not Found: Resource doesn’t exist.

- **Server Errors (5xx)**: Indicates an error happened on the server's end but the problem was not the client's fault.
    - 500 Internal Server Error: Unexpected server error.

Now that you have a handle on the fundamental concepts of what comprises an HTTP request, we'll take at modern conventions and best practices for designing APIs with these concepts and following best practices.