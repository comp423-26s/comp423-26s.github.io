---
authors:
  - Kris Jordan
---

# Staging Server Environment (DevOps)

Your team should setup the staging environment on one team member's namespace. Choose one members' [OKD CloudApps](https://console.apps.unc.edu/) course namespace to setup the production staging environment. The other team member(s) will be added to this namespace as collaborator(s) so everyone has access.

In establishing the staging environment on our cloud infrastructure, we will work from the bottom up. We will start with the database server, then add secrets needed to build and run the application, then add the application, and finally add the route to expose the application to the internet.

## Accessing Cloud Infrastructure

**Warning:** If you are not on-campus when working with the cloud infrastructure, it will have the appearance of being "down". This is due to a firewall preventing off-campus access without a virtual private network VPN connection. If you try to load Cloud Apps at any point this semester and see a non-responsive or blank web page, it is likely because you are not connected via Eduroam nor the VPN.

If you are off-campus, you will need to establish a VPN connection in to make use of Carolina CloudApps: <https://ccinfo.unc.edu/start-here/secure-access-on-and-off-campus/>

Access the OKD CloudApps console here: <https://console.apps.unc.edu/>

Under the **okd** logo, you should see "Developer" in a drop down and to the right "Project: " followed by `comp590-140-25sp-ONYEN` where ONYEN is your UNC ONYEN.

## Using the `oc` Command-line Tool to Administer OKD

The `oc` tool is included in the `csxl` developer container. As long as you are successfully running Docker locally and connected to a campus network or VPN, you will be able to use `oc` from your container. However, if you are making use of CodeSpaces, you will need to install `oc` onto your host machine so that you can access the OKD cluster from VPN/campus rather than the cloud container.

## Logging into the OKD Container

Our course projects will continue to be hosted on the OKD cluster of CloudApps, found here: <https://console.apps.unc.edu/>

Go ahead and log-in. Remember: off-campus access requires VPN as described in the above section!

Next, you will need to log-in to OKD from the Command-Line Utility **in your DevContainer**. The login command is found in the OKD Console. Look in the top right for your name, click the drop down, and select "Copy Login Command". From here select "Display Token". Here, look for the line "Log in with this token" and copy the complete command beginning with `oc login` to your clipboard.

Paste this command into a terminal in your DevContainer (or, if you are on CloudSpaces, your host machine's terminal). You should be correctly logged in and see a message of success.

### Giving Team Members Access to Your Project

One member of each team should be designated the project host. From this member's OKD CloudApps account, you will need to add other team members as follows:

1. Add team members to your course workspace
  * Navigate to the Administrator sidebar (Default is Developer)
  * Select: User Management > Role Bindings
  * For each team member, with their `onyen`:
    1. Create binding
    2. Name: `admin-ONYEN` (replace `ONYEN` with teammate's ONYEN)
    3. Be sure the project you are in in CloudApps is `comp590-140-25sp-ONYEN`
      * `ONYEN` should be your UNC ONYEN
    4. Role name: `admin`
    5. Subject:
      * User
      * Name: your teammate's ONYEN

Add all of your team members and have them confirm that they have access.

### Creating the Database Server

The first step in establishing the cloud deployment is to establish the backend database pod.

1. Add a PostgreSQL database to your project:
    1. Developer View Sidebar
    2. Add (from the Sidebar)
    3. Database
    4. PostgreSQL Provided by Red Hat
    5. Instantiate Template
    6. Change only the following settings:
        1. Database Service Name: `db`
        2. PostgreSQL Database Name: `csxl`
        3. Version of PostgreSQL Image: `latest`
    7. Create
    8. Navigate to the secrets page as described in the next paragraph

Once the database is created, **go to the Secrets page found in the left-hand sidebar and view the generated credentials for the database under `db` (this is the name we gave it above)**. If you select "Reveal Values" you can see the name, username, and password for the database. These secrets will be used as environment variables in your application in the next step.

### Creating Secrets for your Application

Let's create a secret for your application to use. This will be used to store the database credentials, and will ultimately be mounted as environment variables in your application.

Leave open the tab with these secrets, which you navigated to in Step 8 above. Additionally, you will need to generate a random string for the `JWT_SECRET` environment variable. This will be used to sign the JWT tokens that your application will use to authenticate users. You can generate a random string using the following command in your Dev Container:

```bash
openssl rand -hex 32
```

From your DevContainer's terminal, in a shell prompt run the following command to create the secret on OpenShift *BE CAREFUL TO AVOID TYPOS*.

You can copy this command and edit it, replacing the placeholders, in an empty text file before running the command in your DevContainer terminal.

```bash
oc create secret generic final-project-environment \
    --from-literal=POSTGRES_HOST=db \
    --from-literal=POSTGRES_PORT=5432 \
    --from-literal=POSTGRES_DATABASE=csxl \
    --from-literal=POSTGRES_USER=<from-secret-above> \
    --from-literal=POSTGRES_PASSWORD=<from-secret-above> \
    --from-literal=JWT_SECRET=<generate-random-string> \
    --from-literal=UNC_OPENAI_API_KEY=<your-teams-deployment-api-key>
```

For the final secret, be sure to use the team's UNC OpenAI API key you were provided on the print out. It's the last key on the sheet. If this is not accessible, you can also use your own deployment key.

!!! info "Changing Secrets Later"

    If you realize you need to change a secret, you can do so via the OKD web console by navigating to
    
    **Developer > Secrets > `final-project-environment` > Actions > Edit Secret**.

From the OpenShift web console, you can verify that the secret was created by navigating to the Secrets page and selecting the `final-project-environment` secret.

### Deploy Key Secrets

Before OpenShift's builder process is able to clone your repository from GitHub, we need to establish a means for OpenShift to _authenticate_ itself to gain access to your team's private repository. This will closely resemble how _you_ authenticate yourself with GitHub, but with the key difference it's the builder process running on Carolina Cloud app's machines-- not yours!-- that needs to gain access to your GitHub repository.

It is worth pausing to reflect on how sensitive this step is in real world applications: you are setting up a means to directly access your code in a private repository. At organizations you may find yourself employed by, or founding, the code in your private repositories are some of it's most valuable assets and their secure handling is very important to maintaining their secrecy and protecting customers from hacks.

It is for these reasons that you want to be very careful to never commit secrets to a `git` repository. The keys we are about to setup are considered secrets! (If you find yourself at an organization that breaks this rule: run.)

To avoid accidentally commiting secrets to a project, one strategy is to be sure the filenames containing the secrets are added to the project's `.gitignore`. This file lists patterns that will not be included by default. Go ahead confirm the following rule is in the project's `.gitignore` file:

`deploy_key*`

Go ahead and make a commit with this change to `.gitignore` included in the commit.

**DEVCONTAINER:** In your DevContainer's terminal, not your host's, generate an SSH key:

```
ssh-keygen -t ed25519 -C "GitHub Deploy Key" -f ./deploy_key
```

Note: **Do NOT set a passphrase for the ssh key, just press enter at the prompt without typing anything when asked.**

You should now see the files `deploy_key`, which is the private/secret key, and `deploy_key.pub` which is the public key.

Add the public key to your project repository's settings on GitHub:

1. Navigate to your repository's settings
2. Select Deploy Keys
3. Add Deploy Key
4. Title: `CloudApps Deploy Key`
5. Key: Copy the contents of `deploy_key.pub` into the key field
6. Check the box to allow write access
7. Click Add Key

Now run the following command to add the private key as a secret to your Cloud Apps account:

```
$ oc create secret generic comp590-final-project-deploykey \
    --from-file=ssh-privatekey=./deploy_key \
    --type=kubernetes.io/ssh-auth
```

To verify the secret was correctly created, run the following command:

```bash
oc get secret comp590-final-project-deploykey
```

Finally, you need to link the secret to the "builder" process of OpenShift. This will allow OpenShift to use the secret when it pulls your code from GitHub and builds your project.

```bash
oc secrets link builder comp590-final-project-deploykey
```

This command will succeed silently.

### Create the OpenShift Application

IMPORTANT: Be sure you substitute your team's information in TWO places below! First: the repository URL, second the HOST variable should not be `csxl-team-XX`, but should instead be your team zone + number. This is your team's table. Using lowercase is encouraged.

IMPORTANT: Be sure you are currently on your stage branch. If you are not, go ahead and stash and/or commit changes on your current branch, and switch to stage.

```bash
oc new-app python:3.11~git@github.com:comp423-25s/<your-final_repo_name>.git#stage \
  --source-secret=comp590-final-project-deploykey \
  --name=final-project \
  --strategy=docker \
  --env=MODE=development \
  --env=HOST=csxl-team-<TEAM NUMBER>-comp423-25s.apps.unc.edu
```

Notice the `#stage` at the end of the repository URL. This is the branch name that OpenShift will pull from. When setting up the final project, you created a branch named `stage` and established it as the primary branch for your repository. This notion of a staging branch is a common practice in DevOps, and is a good way to keep your production code separate (live at csxl.unc.edu) from your development code (which you are establishing right now).

While the project is building, link the secrets you created as the environment variables of the deployment and verify their existence with `list`:

```bash
oc set env deployment/final-project --from=secret/final-project-environment
oc set env deployment/final-project --list
```

### Exposing the Application

Once your application builds, it will be running on a pod that is not exposed to the internet. To establish a public route, first we need to expose it as a service, run the following command:

```bash
oc expose deployment final-project \
  --port=80 \
  --target-port=8080
```

Next, we can create a route to the service with a specifically chosen hostname. **Please replace `XX` with your team's number  and table number**.

```bash
oc create route edge \
  --service=final-project \
  --hostname=csxl-team-<TEAM NUMBER>-comp423-25s.apps.unc.edu
```

You can now visit the hostname for your team and access it in the browser. If you see a message from OpenShift that says "Application is not available", it means that the application is still building. Once your build completes, you should see the application running, but there is still one more important step: resetting the database.

!!! info "Crash-loop Back-off and 'OOM Killed' (Out of Memory)"

    If your pod keeps crashing, with a message like "Killed by OOM Manager", it's because the Python/FastAPI server process requires more memory than your deployment is configured to provide by default. Our deployment platform, Kubernetes/OKD, monitors resource usage so that its resources are shared fairly among us. It takes a very conservative default, which can lead to your process being crashed when it needs more memory than the default. To ask for more memory, but still a modest amount for 2025 standards, take the following steps in the `oc` tool: 

    ~~~
    oc set resources deployment/final-project --requests=memory=256Mi --limits=memory=1Gi
    oc rollout restart deployment/final-project
    ~~~

    The first command requests a higher memory limit for the deployment and the second restarts the pod in the deployment so that it uses the new settings.


### Resetting the Database

The database that you created in the previous step is empty. You will need to reset the database to the state that it was in when you submitted your final project. To do this, you will need to run the `reset_demo.py` script that is included in your final project repository.

This script needs to be run from within your pod, so in this section you will learn how to connect to your pod and run commands from within it.

First, you will need to find the name of your pod. Run the following command to get a list of pods running in your project:

```bash
oc get pods --selector deployment=final-project
```

You should see a single pod with a name like `final-project-648fdff8d5-rr4fs`. The letters and numbers at the end of the name are a unique identifier for the pod. This identifier changes every time a new build of your pod is deployed, environment variables change, the pod gets restarted, and in other instances. Copy the name of your running pod and run the following command to connect to it:

```bash
oc rsh final-project-YOUR-POD-IDENTIFIER
```

The `rsh` stands for "remote shell".  You are now connected to your pod running in the cloud via a secure shell (ssh)! The commands you run are not running on your host machine, but on the CloudApps infrastructure. If you `ls` you will see you are in your project's built directory. Not everything is there, importantly not the frontend because it was compiled into the `static` directory as part of the build process.

To confirm you are logged into your pod, you can assure yourself with the following command:

```bash
hostname
```

You can now run the `reset_demo` script to reset the database. Run the following command to do so:

```bash
python3 -m backend.script.reset_demo
```

You should see the SQLAlchemy log messages creating tables, inserting dev data, etc. Your staging database is now reset!

**Important**: As you deploy new versions, add new entities, add new dev data, etc., this process of resetting the database in staging is one you and your team members will both need to be comfortable doing and remember to do.

### Setting up Push-to-Deploy Webhooks

GitHub repositories can be configured with webhooks, which are URLs that get called when events occur in order to notify another service of the event. In our case, we want to set up a webhook so that when we merge pull requests to the `stage` branch, OpenShift's build configuration for our project will receive a webhook notification and kick off a new build and deploy pipeline.

To find the URL for the web hook, open up your project in OpenShift and navigate to the Admin sidebar, followed by Builds > BuildConfigs. Select `final-project` and look for the webhooks section at the bottom. Click the Copy URL with Secrets button for the GitHub webhook. This copies the URL to your clipboard.

Next, open your project's settings in GitHub and navigate to Webhooks. Click Add Webhook and paste the URL into the Payload URL field. **Be sure to set the content type to `application/json` and leave the secret field empty.** Click Add Webhook.

From the "Webhooks" page you're brought back to, click your webhook. Then go to the Recent Deliveries tab. You should see a successful delivery. Congratulations, your project is now set up to automatically build and deploy every time your team merges PRs into the `stage` branch! As a reminder, if your data entities change, you will need to reset the database in staging after the build and deploy completes.

### You're in Staging/Production!

This setup mirrors our production setup of `csxl.unc.edu` and is running the same code base. Congratulations on setting up what is, in essence, a production cloud environment for a small, modern web application!

We call this "Staging" in a nod to how many organizations think of "Staging" environments. It's an area where your team can work on a feature, see it deployed publicly on the internet, and test it without having any impact on our production deployment.