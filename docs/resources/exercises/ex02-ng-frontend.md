# Angular Front-end for Link Sharing App

This exercise is a SOLO exercise. Everyone will establish their own repository and work to complete a simple front-end for their own API backend.

In this exercise you will build a web front-end for your Link Sharing API of EX01. In the process you will gain experience with:

0. High-level CORS (Cross-Origin Resource Sharing) Concerns
1. TypeScript:
    * Interfaces
2. Angular:
    * Components
    * Signals
    * Services
    * HttpClient
    * Dependency Injection
    * Routing

## Enabling Cross-Origin Resource Sharing in EX01

### Understanding CORS

CORS (Cross-Origin Resource Sharing) is a security feature implemented by web browsers that restricts web pages from making requests to a different domain than the one that served the original page. This security measure exists to prevent malicious websites from making unauthorized requests to other domains using your credentials.

When you build a web application with a separate frontend and backend (like we're doing with Angular and FastAPI), they typically run on different domains or ports during development. Without proper CORS configuration, your Angular application running on one port (e.g., localhost:4200) won't be able to make API requests to your FastAPI backend running on another port (e.g., localhost:8000).

Additionally, for this exercise, we will deploy your front-end as a static web page on GitHub pages to further emphasize the separation between frontend and backend separation. Your EX02 frontend will run on GitHub Pages and (origin host: comp423-26s.github.io) and backend will run on your personal OKD project hostname. This also requires CORS for requests to succeed across origins.

### Using Middleware in FastAPI

In web frameworks like FastAPI, middleware functions as a bridge between the server and your application code. Middleware intercepts requests and responses, allowing you to modify or process them before they reach your route handlers or before they're sent back to the client.

The `CORSMiddleware` specifically manages HTTP headers related to CORS. When added to your application, it automatically handles setting the appropriate headers that tell browsers to permit cross-origin requests from your frontend application.

In EX02, for simplicity's sake, we will enable **very permissive** CORS settings that are generally far more permissive than you would typically enable in a production application. In essence, we are disabling CORS protection of your API to make integration with our client in this application more straightforward. In true, industrial applications you will specify very specific hosts which you accept CORS API requests from.

### Enable CORS

You will need to add the following code to update your EX01 production deployment to enable CORS for working on EX02. Collaborate with your partner on EX01 to decide who will make this update, push the branch, and make the PR. 

First, import FastAPI's CORSMiddleware module in `main.py`'s imports section:

~~~python
from fastapi.middleware.cors import CORSMiddleware
~~~

Then, register the middleware by adding the following snippet after you define your `app` in `main.py`:

~~~python
# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True, 
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
~~~

Push this to a branch, make a PR, and ask your teammate to merge the PR so they can confirm the work you completed.

## Setting up the EX02 Dev Container

To get started on this project, you will need to accept and clone the EX02 starter repository here: <https://classroom.github.com/a/ZInataQQ>

Once cloned, open the project in a dev container and wait for the post create build steps to complete. 

Start the development server with the following command:

~~~bash
ng serve --host="0.0.0.0"
~~~

You may need to press enter to a prompted question about autocompletion rules. Just accept the default suggestion.

The `host` flag instructs the Angular development server to listen on all IP addresses (0.0.0.0) for requests, which ensures Docker is able to route you through from your host to the dev container.

Open <http://localhost:4200> and you should be greeted with a simple user interface with some code to help get you started with this project.

### Starter Code Orientation

#### Core Files

* `src/main.ts` - Application entry point that bootstraps the Angular app
* `src/app/app.component.ts` - Root component that serves as the application shell
* `src/app/app.routes.ts` - Defines the application's routing configuration

#### Components

* **Share Component** (`src/app/share/`):
    * `share.component.ts` - Form implementation using Angular Reactive Forms and Signals
    * `share.component.html` - Template with resource type selection and content input

* **Navigation Component** (`src/app/navigation/`):
    * `navigation.component.ts` - Simple navigation logic
    * `navigation.component.html` - Navigation links using Angular's router directives

## 1. Implement Sue's Stories

Your task is to introduce an angular Service object that integrates with your API in order to complete the implementation of the `ShareComponent`, which will make use of the Service.

The general strategy for making progess here is:

1. Read and understand what is going on in the Share Component's TypeScript controller and HTML view template.
2. Generate a Service (hint: use `ng generate service` subcommand).
3. Define a method on the service for creating a link and/or snippet. It should take the appropriate parameters (which will be provided by the component) for creating a resource for your API (e.g. the type of resource and the content of the resource).
    * Assuming your API end point for Sue just returns a string, this method should return an `Observable<string>`, which will represent a shortened URL. If your API returns an object with properties, you will need to define an `interface` that has thoes properties and give it a name. Your method would return `Observable<YourInterfaceName>` instead.
    * For now, you can implement a fake skeleton of the method by having it return `of("https://foo.bar")` by importing the `of` function from `rxjs` (read more about `of` here: <https://rxjs.dev/api/index/function/of>). If your API returns an object, you can return an anonymous object with the expected fields, such as `of({"url":"https://foo.bar"})`;
4. Inject your service into the `ShareComponent`'s constructor as a private variable.
5. Update the submission logic to call out to your service object's method(s) _and subscribe to the result_ as you read about in the HttpClient reading: <https://angular.dev/guide/http/making-requests#fetching-json-data>. For more information on how to subscribe, see the official RxJS documentation: <https://rxjs.dev/guide/observer>.
6. Ultimately, you will need to update the `ShareComponent`'s controller and HTML template upon success (or failure...) of the service method such that the template displays the resulting URL generated by your API. You should be able to click the URL and be taken to a new tab (make it an `a` tag and set the `target` attribute to `"_blank"`).
7. Now it's time to actually implement integrating with your production API! You will need to inject `HttpClient` into your service, as is discussed in the `HttpClient` setup documentation <https://angular.dev/guide/http/setup>. Then, in your methods, replace the call to `of` with a call to your injected `httpClient`'s `post` method, like you read about in the ["Mutating server state"](https://angular.dev/guide/http/making-requests#mutating-server-state) of the Angular HttpClient Reading. You will need to provide a request body object which contains all necessary information for your API.
8. Try it! One of two things will happen:
    * Nothing or an error. Open your Chrome Developer Tools and look in the console and the network tab for more diagnostics on what is going on behind the scenes. The network tab will be your best tool here. Investigate the tab. Not seeing your request? Be sure `Fetc/XHR` is shown. Still not seeing it? Did you save everything and `subscribe` to the result of your service method call from your component? Remember, the returned value from your service method is an `Observable` not an actual result! Seeing an error? Look at the HTTP response code to diagnose. If it's a CORS issue, return back to the CORS steps above and be sure you successfully deployed. If it's a 422, it means your request body did not fulfill the expectations of your API from EX01. Be sure you are sending all the data you need!
    * Success: Woo! Sue will be so happy to use your new UI rather than the `/docs` UI!

## 2. Implement Resource List Link

For the second required portion of this exercise, you will introduce a new routable component for listing resources in your backend API for Amy. No filtering user interface is required. We'll make this functionality visible to all users, though, since this is just a demo application.

Your goal here is to add a new item to the navigation for a resource list, add a component that you get routed to when viewing the resource list, and add additional service functionality and control templating for displaying all resources stored in your backend API.

The general strategy here is to:

1. Generate a new component (`ng g component`)
2. Make the component routable via `app.routes.ts`
3. Add a link to `navigation/navigation.component.html` so that you can navigate to the component
4. Inject your API service into your component (like you did in `ShareComponent`)
5. Implement a skeleton of a method in your service for listing resources from your API. Is should return type `Observable<YourAPIResponseType>` where `YourAPIResponseType` is an interface you define to match your API's expectations. It may also be `YourAPIResponseType[]` if your API returns a list of the response and not an object.
5. Implement the lifecycle interface [`OnInit`](https://angular.dev/api/core/OnInit) that gets called when a component is loaded (in this case: routed to). This will subscribe to the service class' method. It should update one or more signal(s) you define in the class.
6. The values of those signals should be read by the HTML template so that the resulting list of resources in your API are produced to the view layer of the system and you can see them in a table format.

When deciding what and how to show the information on this screen the question you should ask yourself is, "what would I want to see if I were Amy Admin?"

## Publishing

The project comes predefined with a GitHub Action for publishing your web site. You will need to enable GitHub Pages for your project, though. To do so, go to your project's settings, go to Pages, and turn pages on from the `gh-pages` branch. It will take a couple minutes for this to take effect. You should be able to follow with the publishing process in the Actions tab. Once publishing is fully ready, you should see a link to your website if everything built correctly.

## Branch Expectations

You are encouraged to experiment in branches while making progress on this exercise. However, your `git` workflow in this exercise is up to you. Ultimately, we expect your final product to be on `main` since that is what will be deployed live.

## Required Angular Conventions

No credit will be given to projects which use old Angular style `ngIf` or `ngFor` tags, you should use the `@if` and `@for` functionality we read about. Additionally, all data that is shared between a `Component` typescript file and its HTML template should be done so via modern angular `signal`s, like you read about.

## Extra Credit

The following opportunities are available for extra credit, arranged by least to most challenging:

1. 1pt - Implement Vanity URLs in the Frontend
2. 1pt - Implement Expiration Dates when sharing a URL in the Frontend
3. 1pt - Implement Amy's Filtering Stories in the List Resources View
4. 2pt - Implement all of Amy's Stories (update, delete, view access counts)
