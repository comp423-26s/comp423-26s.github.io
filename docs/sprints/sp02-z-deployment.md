---
code: SP02
title: Deployment Instructions
ate: 2026-04-20
due: 2026-04-27
type: sprint
threads: ["Design"]
authors: [Kris Jordan]
---

Your team will need to choose a team member to serve as the primary account holder / dev ops lead. They will need to add the other team members to their account. To do so:

## Staging Hotfix

We needed to add an additional environment to the project for staging purposes. The staging setup allows us to login as other users:

- `git switch -c hotfix-stage`
- `git fetch --all`
- `git cherry-pick f7ddbaf` (this should not result in conflicts, but if it does you will need to carefully resolve them) - if this fails, you will need to be sure you have `upstream` added as a remote that links to `https://github.com/unc-csxl/learnwithai.unc.edu.git` and then fetch all again
- `git push origin hotfix-stage`
- A team member will need to CR and merge
- You will need to then switch back to `main` and pull the latest and you should be all set to deploy to staging.

## Adding Team Members

After you've decided whose account will be the main deployment account, that team member will need to do the following:

1. Log in to OKD <https://console.apps.unc.edu/> (if you are NOT on Eduroam, you will need to be VPN'ed in)
2. Under Home > Projects look for your project named `comp423-001-26ps-<ONYEN>` where `<ONYEN>` is yours. Select this project.
3. Navigate to User Management > Role Bindings. Click "Create Binding".
4. For each member of your team:
    1. Name: `admin-<ONYEN>` where the `<ONYEN>` is your teammates ONYEN
    2. Namespace: select your project
    3. Role: `admin`
    4. Subject name: your teammate's ONYEN
5. After adding each teammate, they should be able to see your project in OKD.

## Setting up Secrets

### Secrets

In your `infra` directory, make a copy of `manifests/secrets.example.yaml` to `manifests/secrets.yaml`. From here, you will need to replace the placeholder values, these are the all caps words that are surrounded by greater than and less than symbols, like `<DB_PASSWORD>`

!!! danger Do *not* replace `${NAMESPACE}`
    This is a template variable that needs to stay as is in order for the deployment scripts to correctly target _your team's namespace_ which will be substituted in from a command line argument when you deploy.

The placeholders you need to replace are the follow. We recommend these simple values for our staging server setup. Once you have yours established, you can share with your teammates so that everyone is using the same secrets if they need to redeploy for some reason.

`<PUBLIC_HOSTNAME>`: This will be your team's staging hostname: `https://team-<TEAM>.apps.unc.edu` where `<TEAM>` is your table (eg `a1`)
`<DB_PASSWORD>`: `postgres` (Note: there are multiple places to replace this placeholder!)
`<RABBITMQ_PASSWORD>`: `rabbitmq` (Note: there are multiple places to replace this placeholder!)
`<GENERATE_A_STRING>`: it is worth having a strong random value here, search the web for a UUID generator
`<AZURE_OPENAI_SUBSCRIPTION_KEY>`: use the key of the member who is hosting the deployment
`<AZURE_OPENAI_DEPLOYMENT_NAME>`: set this to `gpt-5-mini` unless you have other model specific needs

<!--
### Environment `development` Override

These configuration settings are established for how we would typically deploy in production. However, for our course purposes and demo purposes, the ability to authenticate as test users (like Ina and Sally) is useful. By using the development environment settings, we will get the handy "Login as" button on login and the routes for logging in as other users without security hangups are revealed.

To override the environment of our app and worker pods, open their `yaml` files in the `manifests`: `app.yaml` and `worker.yaml`. Look for their `env` section where the environment variable of `ENVIRONMENT` is set to `"production"`. Change this setting to `"development"` in both files.
-->

## Logging in to OKD in your DevContainer

Your devcontainer is equipped with the `oc` command-line utility that allows you to control OKD/Kubernetes clusters. You need to login with a token on your devcontainer for the commands to work, though. To get the login token:

1. Open OKD in your browser (<https://console.apps.unc.edu/>).
2. Click on your onyen top right corner.
3. Select 'Copy Login Command'
4. Display Token
5. Copy the command beneath "Login with this token"
6. Paste it in the terminal of your devcontainer
7. Confirm you are logged in with `oc project`. You should see your namespace if you are the devops lead on your team, otherwise switch to your devops lead's namespace with: `oc project comp423-001-26sp-<ONYEN>`

## Running the Initial Deploy Script

You will need to open a terminal in your devcontainer inside of the `infra` directory.

Here you will see two important subdirectories:

- `manifests` - these are the declarative configuration files which declare the structure of our deployment
- `scripts` - these shell scripts utilize the manifests and the `oc` command-line program to apply the configuration to open shift and carry out common tasks like deploying, resetting the database, and destroying the setup

Try your first deploy:

1. `bash scripts/deploy.sh comp423-001-26sp-<ONYEN>` where `<ONYEN>` is substituted with your team's dev ops lead's ONYEN. Only your devops lead should need to run this command. Rerunning it will cause a new deploy key to be generated which will break your build without updating it.
2. You will be prompted with some required manual **source-clone deploy key** setup. **BEFORE YOU PRESS ENTER** navigate to your team's project on GitHub. Go to its **Settings**, **Deploy Keys**, **Add deploy key**, use the suggested title for the title, then copy from the command-line the complete line beginning with `ssh-ed25519` into the **Key** value in GitHub.
3. Do not check Allow write access
4. Select **add key**. This is effectively setting up a public/private keypair that allows OKD to read your team's repository to make builds for future deployments.
5. Open a tab back to your OKD Topology for your project (it will be empty, but after the next step you will see the deploy take shape)
5. Press enter back in the command-line deploy script
6. It will take some time for each of the pods and builds to complete, take note of the steps going on by watching both the topology visualization of your app being deployed as well as the command line progress updates.
7. After the build succeeds (green check on `learnwithai-app` pod), you will need to add a custom route to make the app navigable:
    1. Networking
    2. Routes
    3. Create Route
        1. Name: The autogenerated name is fine
        2. Hostname: Paste in your HOST value from secrets.yaml (`team-<TEAM>.apps.unc.edu`)
        3. Path: `/`
        4. Service: `learnwithai-app`
        5. Service weight: leave as 100
        6. Target port: 8000
        7. Check secure route, TLS termination **Edge**, insecure traffic **Redirect**
        8. Create

## Resetting your Database

Now, we need to roll out your database reset script so that the postgres database is initialized with the correct tables and seed rows.

Back in your dev container's commandline, in the `infra` directory, run the script:

`bash scripts/reset_db.sh comp423-001-26sp-<ONYEN>` where `<ONYEN>` is your team's dev ops' ONYEN. This script should succeed.

## Testing your Deployment

Finally, you should be able to navigate to your deployed hostname in your browser.

## Deploying new Commits / Builds

There are two paths toward deploying new builds in OKD. The manual path is to go to Builds, BuildConfigs, select `learnwithai-app`, and under the actionsn drop down select `Start Build`. When the build completes, you will see it roll out to your app and worker in the topology view. Note that you should not expect different results for a subsequent build unless there are new commits in your repository on GitHub.

The automated "continuous deployment" path toward building when you land a PR into main is to add a webhook to your GitHub repository's settings. In OKD you can find the webhook by navigating to: Builds, BuildConfigs, `learnwithcli-app`, Scroll down to Webhooks, and (confusingly, but more predictably) copy the Generic URL with Secret button. On GitHub, navigtae to your repos settings, Webhooks, Add Webhook, paste the URL into Payload URL. Leave the other settings default and add webhook.

## Development Settings and Auth-as-User

We are working on a fix for deploying to CloudApps in such a way that it mirrors your development experience of being able to easily change users. We will announce the steps to deploy in development/staging mode later today, it will be a minor patch to land in your project.