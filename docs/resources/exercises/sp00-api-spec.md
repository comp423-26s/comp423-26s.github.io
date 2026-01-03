# Sprint 1 - Week 1 - Interactive Prototypes & API Scaffolding

Now that your initial feature design document and mid-fi wireframes are in place, your team will extend your work by developing interactive, clickable prototypes. These prototypes will enable your team to clearly demonstrate user interactions, providing peers with tangible insights into your feature’s workflow. These clickable prototypes will be high fidelity and utilize the [Material 3](https://m3.material.io/get-started) design system of the CSXL. Additionally, you'll start scaffolding out the backend API routes and models necessary for your feature using FastAPI as the foundation.

## Assignment Details

### 1. Clickable Prototypes

- Choose your primary user stories and their wireframes from last week to convert them a **high fidelity wireframes** using the CSXL Figma template.
    - Duplicate the [CSXL Figma template](https://go.unc.edu/csxl-figma) into one of your team members' Figma spaces and add your team members to it.
    - Add your story to the `Getting Started + YOUR DESIGN` page. Copy starter pages from **CSXL Design** page and material components from **Components**.
    - We expect to see Material components and design principles followed throughout, unlike in the lo/mid-fi wireframes produced last week.
- Turn your high-fidelity wireframes into a clickable Figma prototype as shown in class.
- Clearly illustrate the interactions from your top 3 critical user stories.
- Ensure each clickable prototype demonstrates:
    - The sequence of interactions.
    - Where your feature will use the OpenAI LLM API.
    - Key interactions or critical decision points clearly presented.
- Link each clickable prototype clearly within your stories in your design document (Google Docs, Notion, etc.).
- Be prepared to present your top two story prototypes in a concise, 5-minute demonstration during class on Monday, March 31st. For each presented user story, include:
    - The associated REST API route(s) (next part).
    - The model(s) it utilizes.

!!! tip "Prototype Presentation Advice"

    - Clearly narrate your user's journey through your prototype.
    - Highlight the value your feature provides through specific interactions.
    - Keep explanations clear and to-the-point to manage your time effectively.

### 2. REST API & Model Scaffolding
Begin detailing your API in your design document by:

- Defining REST API routes that clearly support your critical user stories.
- Describing new models your feature's REST API will require. Refer to existing models located at `backend/models` in the CSXL repository to guide your designs.
- Clearly indicate if existing routes or models will need augmentation or modification.

Your document should clearly communicate:

- Route HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) and paths.
- The purpose of each route.
- Basic descriptions of the data each route will handle.

### 3. Integration Analysis
Answer the following critical integration questions in your design document:

- **Existing Dependencies:**
    - Identify specific files, classes, and methods your feature's starting point will directly depend upon, extend, or integrate with. Provide permalinks (including line numbers) from the [CSXL codebase](https://github.com/unc-csxl).
- **API & Models:**
    - Clearly cite where you plan to add routes (new files are acceptable, but provide their complete paths).
    - Clearly cite where you plan to add or modify models.
- **Frontend Components:**
    - Identify how you will organize your frontend component(s).
- **AI Prompts:**
    - Behind the scenes your backend will need to make requests to the OpenAI API (think: ChatGPT). Start to brainstorm the prompts your backend routes will use with the AI, in other words: what would you put into the ChatGPT chat box and expect back. A common strategy is taking some user text and [converting it into a structured JSON output you specify](https://platform.openai.com/docs/guides/structured-outputs).
    - Identify at least one prompt and the JSON model format you expect as a response from the OpenAI API. Give some sample input text or JSON data from user inputs, representative of what your backend would send to the OpenAI API, and provide concrete examples of expected responses.

Clearly identifying these dependencies and frontend needs early will streamline your future development and avoid surprises.

### Project Management Best Practices

On Wednesday, we'll provide instructions for setting up your team's project board on GitHub. We'll dedicate class time on Friday to discussing GitHub issues and project board best practices. Keep the following in mind:

- Tasks should be clearly described, assigned to team members, and updated frequently.
- Link each project board card to relevant issues in your GitHub repository.

!!! success "Why Project Management Matters"

    Using structured project management practices from the beginning will improve:

    - Team coordination and productivity.
    - Code quality through continuous peer review.
    - Your shared understanding of the codebase and collaborative skills.

### Team Project Setup

Your team will share a GitHub repository for collaboration. This repository is where you all will create pull requests, perform code review, and establish a continuous deployment pipeline (next sprint).

1. To get started, designate one member of your team to establish the repository. This member will create a new team named after your assigned team table, e.g. **Team A1** if you are assigned table A1. See the [teams sheet](https://docs.google.com/spreadsheets/d/17hDPg7UlSqmrmPqvYOTcOW5oIE4Za4ICIRfXCZrzjq4/edit?gid=0#gid=0) to verify your team table. Then, follow [this link to establish your team](https://classroom.github.com/a/ZpRSh22I) and create a blank, starter repository. Once this is completed, other members of team should join the team and the repository.

2. Another member of the team should be designated for the initial repository push. This team member should have already joined the team and should be able to see the blank repository accepting the assignment resulted in on GitHub (named after your team table). As part of RD26, you setup a local development environment for the CSXL. You should open that dev container and go ahead and pull from origin one more time to get the latest updates from the upstream CSXL repository. Go ahead and _remove_ the remote repository named `origin` from your repository. Then, add a new remote repository named `origin` that is directed at the `https://github.com` URL of your final project. Go ahead and push `main` to `origin` and confirm that your team's repository now has the complete history of the CSXL repo in it. You will see a latest commit from your TA Andrew (`ItIsAndrewL`) as the most recent commit with ID prefix `a46bf64`.

3. After completing step 2, all other members of the team should update their local CSXL development environment to remove the git `origin` remote and establish a new remote, named `origin`, that points to your team's GitHub repository (use the `https://github.com` URL). After doing so, you should be able to perform `git pull origin main` and it succeed. Additionally, you can verify correctness by running `git remote show origin` to see that it is pointed to your team's repository and not the official CSXL repository.

4. Only after everyone has successfully completed step 3, a third member of your team should establish a project board for your team.
    1. Begin by opening you your team repo (`comp423-26s/csxl-team-XN` where `XN` is your table number, like `a1`). 
    2. Be sure you do this from your team's repository page! From this page, click the `Projects` tab. Click `New Project`. 
    3. From the modal with templates, select `Featured` and then select the `Kanban` template. 
    4. Name the project "Team XN Project Board", where XN is your table. 
    5. Finally, press the ellipses `...` in the top right corner, beneat your profile photo, and select **Settings**. 
    6. Click **Manage Access** and under "Invite Collaborators", search for your team, select it, make the role Admin, and click Invite.

5. After completing step 4, other members of the team should verify they are able to access the team project board by going to the repository on GitHub, clicking the Projects tab, seeing the project show up there and able to navigate to it.

We will discuss setting up your project board in class on Friday 3/28.
 
### Submission & Demonstration

- Continue updating your original design document.
- Ensure all clickable prototypes are clearly linked to from within your user stories. Test these links in an incognito window. You should be taken directly to the start of a story clickthrough.
- Be ready to demonstrate your clickable prototypes clearly and succinctly on March 31st, including clear references to routes and models associated with each story.

This structured, design-forward approach will enhance both the quality and manageability of your feature, setting a strong foundation for the development cycles ahead.