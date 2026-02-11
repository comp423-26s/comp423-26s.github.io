---
code: RD15
title: "Toward Designing and Formally Specifying APIs"
date: 2026-02-11
due: 2026-02-12
type:  reading
threads: ["System / APIs"]
authors: [Kris Jordan]
---

# 5. Toward Designing and Formally Specifying APIs

Now that you have seen the key elements of HTTP at a conceptual level, across the entire request-response journey, let's focus in on how API designers generally use the inputs from a request. Additionally, let's look at how responses are designed.

When working with HTTP APIs, there are multiple ways to provide input to a request, each serving a different purpose:

- **Methods** define the type of action the API request is performing.
- **Paths** define the structure of an API and uniquely identify resources.
- **Query Parameters** allow clients to filter, sort, or refine results without changing the resource's identity.
- **Bodies** are used to send structured data in requests, typically for creating or updating resources.
- **Headers** provide metadata about the request, such as authentication details or content type preferences.

Understanding these inputs is essential for designing HTTP APIs that are intuitive, efficient, and scalable.

## Introduction to REST

**REST (Representational State Transfer)** defines a set of architectural principles for designing HTTP APIs that focus on resources and how to design interactions with them. 

REST emerged from Roy Fielding's 2000 PhD dissertation, where he formalized the architectural principles that had guided his work on the [HTTP specifications](https://www.w3.org/Protocols/HTTP/1.0/spec.html). While working on HTTP standards, he observed that many distributed systems at the time were tightly coupled, requiring detailed knowledge of each other's internal implementations. His dissertation introduced REST as an architectural style that embraced the web's fundamental design - particularly its use of **hyperlinks as resource identifiers**, **standard methods** (such as GET, POST, PUT, DELETE, and so on), and **stateless communication**. What made REST revolutionary was that it showed how to build distributed systems that could evolve independently by following these principles, allowing clients and servers to evolve and change without breaking each other. This was in stark contrast to earlier approaches that required lockstep changes between clients and servers.

A key characteristic of REST is that it's **stateless**—each request from client to server must contain all the information needed to understand and process the request. The server shouldn't need to remember anything about previous requests.

HTTP APIs that embrace this architectural style are often described as being _RESTful_.

### Resources and Their Role in RESTful APIs

In RESTful APIs, the nouns in your API are **resources**. Each resource is uniquely identified by a **URL (Uniform Resource Locator)**, meaning every resource has its own address.

You may know these as web addresses, like:

- [https://csxl.unc.edu/api/organizations](https://csxl.unc.edu/api/organizations) → Returns a list of CS student organizations in JSON.
- [https://csxl.unc.edu/api/academics/section/term/26S](https://csxl.unc.edu/api/academics/section/term/26S) → Returns a list of CS classes offered in Spring 2026.

!!! warning "Could you easily see the structure of the JSON in the URLs above?"

    Most web browsers don't have nice, automatic formatting of JSON data. If you open the links above and it's not easy to see the structure of the data, we **strongly** recommend installing a web browser plugin to format JSON data. They are super handy when designing and building your own APIs!

    In Google Chrome, for example, we recommend [JSON Formatter](https://chromewebstore.google.com/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa). Other browsers have similar tools—find one with good reviews and many installations.

## Request Input Specifications

### Methods: Defining Actions

The **method** of an HTTP request tells the server what action is being performed on the resource. You previously read about the fundamental API methods in the last section, including **GET, POST, PUT, PATCH, and DELETE**. While we won't go into detail here, it's important to recognize that the method is an essential input to an HTTP request and characterizes the request's _intent_ to read, write, delete, or update.

### Paths: Identifying and Routing Requests

The **path** of a URL is technically just an opaque string of characters. You could design APIs with any scheme you'd like, but most REST API designers today model it as a **logical hierarchy**, much like folders in a file system:

- `/api/users` → Might represent a collection of users.
- `/api/users/42` → Might represent a specific user with ID 42.
- `/api/users/42/orders` → Might represent orders placed by the user with ID 42.

A path tells you which resource you want to work with in an API. For example, `/api/users/42` points to a specific user.

Paths often contain both static and dynamic parts. In the example above:

* `/api/users/` is static - it's always written exactly this way
* `42` is dynamic - it changes based on which user you want

When you build an API, your framework (e.g. FastAPI in COMP423) handles **routing** - matching each incoming request to the right piece of code. The framework looks at two key inputs:

1. The path (what resource you want)
1. The HTTP method (what you want to do with it)

For instance, sending `GET` vs `DELETE` to `/api/users/42` will trigger different actions, even though the path is the same. GET might retrieve the user's information, while `DELETE` might remove their account.

Using a common delimiter character, like the `/` character in a path, communicates subparts of a path to both humans and the system. This convention allows us to visually read the parts of a path and it also allows for programs to _parse_ the path in a straightforward manner by breaking the string up by its `/` characters.

### Query Parameters: Refining Requests

HTTP API designers aim to use query parameters when you need to customize what data is returned back from an API resource. They are added to the end of a URL after the path and tell the server how to filter, sort, or modify the data before sending it back.

Here's how they work in a URL:

```
www.bookstore.com/books?genre=fantasy&sort=newest
```

The path of this request is `/books`, a resource that lists all books being sold by a hypothetical book store.

The query parameter begans at the `?` following the path:

- Each parameter has a name and value joined by `=` 
- Multiple parameters are connected with `&`

Like parameter passing to a function, query parameters allow the same resource to inform its behavior and response. Common uses include:

- Filtering: `?genre=fantasy` (only return fantasy books)
- Sorting: `?sort=newest` (arrange by newest first) 
- Pagination: `?page=2&limit=10` (get 10 items from page 2)
- Searching: `?search=dragon` (find items containing "dragon")

The server reads these parameters and adjusts what data it sends back based on them.

APIs that use query parameters will often have default values for each parameter so that requests without them will still succeed. For example, when loading the first page of a product listing API, your request may not need the `page` parameter, but on pages `2` and `3` beyond, it does.

Beyond APIs, query parameters are a fundamental part of the web. A common example is a Google search URL:

- `https://www.google.com/search?q=REST%20API` → Searches Google for 'REST API'. Here the `q` is the name of the query parameter, Google's short-hand for _query_, and `REST API` is the value.

You, as the designer and implementer of an API, will decide whether any of your routes utilize query parameters and be responsible for modifying responses based on their values.

### Path and Query Parameter Design Conventions

Over the past 25 years, API designers have found many conventions in deciding how to name parts of a path, and how to use path and query parameters together.

🎯 Target nouns, not verbs - resources are things, not actions:
```
✅ /articles
❌ /getArticles
```

🎪 Use plural nouns for collections:
```
✅ /users
❌ /user-list
✅ /users/123
❌ /user/123
```

🎭 Pick a form and stick to it - be consistent with plurals:
```
✅ /posts/123/comments/456
❌ /posts/123/comment/456
```

🌲 Don't nest too deeply:
```
✅ /articles/123/comments
❌ /articles/123/comments/456/replies/789/likes
```

🐪 Use kebab-case or lowercase:
```
✅ /blog-posts or /blogposts
❌ /blogPosts or /blog_posts
```

🔍 Filtering goes in queries - use parameters for modifiers:
```
✅ /articles?status=published&sort=date
❌ /published-articles-sorted-by-date
```

🎯 IDs belong in paths, not query parameters - directly access resources:
```
✅ /users/123
❌ /users?id=123
```

👨‍👩‍👧‍👦 Family trees make sense - use nesting for real hierarchies:
```
✅ /teams/123/members
❌ /members?teamId=123
```

As you get deeper into API design and implementation there are a few other best practice, as well, but if you merely followed these for the purposes of this course you will be doing great.

### Bodies: Sending Data in Requests

For **POST** (creating) and **PUT** (updating) method requests, we need to send more complex data to the server. This data is sent in the **body** of the HTTP request, often in JSON format:

```json
{
  "name": "Alice",
  "email": "alice@example.com"
}
```

When designing the specification for an API, we will need to clearly define a _schema_ for bodies. A schema defines exactly what "shape" of data our API expects in the request body, such as field names, data types, and structure. In the example above, the structure is a single JSON Object (denoted by the surrounding curly braces), the field names are `name` and `email`, and both fields expect `string` values assigned to them.

Unlike paths or query parameters, **bodies are not visible in the URL** and can contain more complex structures like lists and nested objects. As such, sending `POST`/`PUT` requests to APIs is more involved than `GET` requests. Either you have to use a tool, which we'll look at an example of very soon, or you have to write some API client code.

### Headers: Metadata for Requests

HTTP **headers** carry additional standard metadata about the request. The names of the example headers shown below are all defined by the HTTP standard. The API designer's use of headers is _primarily_ choosing which standard headers to utilize, if any. 

- **Authentication** is used to prove the request is made by an authorized user (e.g. Bearer Tokens for security):

  ```http
  Authorization: Bearer abc123xyz
  ```

- **Content-Type** tells the server the data format in the request body (e.g., specifying JSON data format):

  ```http
  Content-Type: application/json
  ```

- **Accept** indicates the client expects a certain data type in the response body (e.g., requesting a response in a specific format):

  ```http
  Accept: application/json
  ```

In the initial APIs you design, you will not be overly concerned with headers. Why? We will start with building some public APIs that do not attempt to authenticate a user. Additionally, all of our APIs will standardize around the `application/json` request body and response format. It's become pretty standard and is nice to work with. If you spend enough time implementing APIs, you may find it interesting to learn more about _content negotiation_ which allows the client to request the same resource be responded in a specific data type (such as `XML` or `HTML` rather than `JSON`).

Headers are also commonly used to help out with content caching, where clients give servers a hash of their cached content and servers can response "nothing's changed, reuse your cached copy and we're not sending anything else back." Additionally, headers are used for some security features as well, like preventing an old phishing attack where an unsuspecting person would be presented with what looked like a benign form, press submit on the form, and actually have the user submitting a POST request sent to their bank's web site to transfer money from their bank account or make a purchase on an web store. That is referred to as "cross-site request forgery" or CSRF. Headers can play a role in protecting APIs against it.

In some avante garde APIs, designers may introduce their own custom headers, which you can spot as different from standard headers using an `X-` prefix, such as `X-API-KEY`, but this is rare and certainly not something you should consider when designing early APIs. If you were ever to think, "hmm should I design a custom header for this?" the answer is probably no and the extra information should be bundled in a request either as a query parameter or additional field in the request body.

## Response Output Specifications

After a client makes a request to a server, the client needs to know what kind of response(s) to expect back in order to properly handle the response. What is the happy path? What is expected when something goes wrong? Typically response specifications are pairings of _response code_ and _response body schema_. For example, if a client provides a well formed request to search for a user in a directory, it can expect to receive back a `200 OK` response code and a JSON response body with a user schema. If a client fails to provide a necessary query parameter, perhaps a `400 Bad Request` response code is sent with a JSON response body that includes an _error schema_ with different fields than a _user schema_ indicating what went wrong.

### Response Status Code

These were covered in more detail in the previos reading. Typically your job as an API designer is to specify which codes a resource routes (method + path) may respond with. 

Success Responses (200-299):

- You must specify what data will be returned (the response schema)
- Example: A 200 response returning user data needs a schema defining the user object structure

Redirection Responses (300-399):

- No schema needed
- The next location is sent in the response headers instead
- Example: A 301 response includes a header pointing to the new URL

Client Error Responses (400-499):

- Need a schema for error information
- Many API frameworks provide default error schemas
- Example: A 400 response needs a schema showing how error messages are formatted

Server Error Responses (500-599):

- These represent unexpected failures
- Examples: Server crashes, out-of-memory errors, database connection failures
- Generally don't need custom schemas since these are unplanned errors
- Your framework typically handles how these errors are formatted

As an API designer, you'll mainly focus on defining schemas for success responses (200s) and client errors (400s), since these are the planned, normal operations of your API.

### Response Body Schemas

Just like with _request body schemas_ discussed above, an API Designer is tasked with specifying the shape of data clients can expect in response to their request. This is _very analagous_ to specifying the return type of a function or method when programming. In most modern API frameworks, including the one you will learn in this course (FastAPI) the way we specify request and response body schemas is exactly the same and will be _very comfortable_ to you. Why? Because they'll just be class definitions!

### Response Headers

Like request headers, your initial API design work will not be overly concerned with response headers. Why? We'll always respond with a content-type of JSON. Additionally, many advanced response headers (cache control and compression) are handled by middleware and configuration, not explicitly our concern when designing the structure of an API. It's unlikely you'll need 300-level response codes in your first APIs, but these would be a reason you would care about headers: when you _redirect_ a client because a resource URL has moved that information is sent back via a `Location` header. When the time comes, trust a quick documentation search or LLM prompt will fill you in.

## Kris, can we _please_ just code up an API?

Yes! I promise if I believed starting with writing API code first, before these concepts were introduced and vaguely familiar, that it is easy to fail to get lost in the details. Modern API frameworks, like FastAPI, go to great lengths to make the developer experience as convenient and terse as possible. Some of these inputs (like the difference between a dynamic path part and a query parameter) can be hard to spot the differences of, or know why to use one over the other, when writing your first API implementation code. Keep these inputs and specification concerns in mind as we dive in next!