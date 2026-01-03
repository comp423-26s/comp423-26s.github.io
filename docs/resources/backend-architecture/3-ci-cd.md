# 3. Introduction to CI/CD

Modern software development moves fast. Teams need to deliver features quickly, fix bugs rapidly, and maintain high-quality code—all while ensuring deployments are smooth and reliable. This is where **CI/CD** comes in.  

- **Continuous Integration (CI)** automates the process of running tests on new code changes whenever they are pushed to a central repository. This ensures that issues are caught early and developers get fast feedback. It can also be used during a Pull Request workflow to prevent a branch from being merged into `main` until it passes all tests.
- **Continuous Deployment (CD)** takes things a step further by **automating the deployment of every successfully tested change directly into production**—without manual intervention. This allows teams to ship updates multiple times a day with confidence.  

!!! note "Continuous Delivery vs. Continuous Deployment"  

    **Continuous Delivery** ensures that every tested change is ready for deployment but still requires a manual approval step before going live. **Continuous Deployment**, on the other hand, removes this manual step and automatically pushes changes to production once they pass all verification checks.  

    In this tutorial, we’re focusing on **Continuous Deployment**, where code moves to production immediately after passing CI tests.  

## Why CI/CD Matters  

Manually running tests and deploying software can be slow, inconsistent, and prone to human error. CI/CD automates these critical steps, leading to:  

- **Faster development cycles** – Developers can push changes more frequently without worrying about breaking things.  
- **Less anxiety** – Automated testing and deployment remove the guesswork, making releases predictable and repeatable.  
- **Higher confidence** – If every change is tested and verified before it reaches production, teams can move forward with fewer worries about stability.  

By embracing automation, teams shift from a culture of hesitation and uncertainty to one of confidence and speed. Instead of fearing deployment days, developers can focus on building great software.  

## How Continuous Integration (CI) Works  

CI ensures that every code change is automatically tested before being merged or deployed. When a developer pushes code, a CI system:  

1. Detects the change  
2. Automatically runs tests  
3. Reports results, allowing developers to catch and fix issues early  
4. Prevents merging into the main branch (if using pull requests) or deployment if tests fail  

A tool like **GitHub Actions** can be used to define workflows that trigger these tests on every push or pull request. If tests fail, CI can block the code from being merged or stop the deployment process, ensuring that only properly tested changes move forward.  

## How Continuous Deployment (CD) Works  

Once CI verifies that code changes pass all tests, CD ensures those changes are **automatically deployed to production** without human intervention. A system like **OKD (OpenShift Kubernetes Distribution)** or **Kubernetes** can handle deployment by:  

1. Being notified of `CI` successfully passing all tests on `main` and receiving a webhook callback
2. A `BuildConfig` begins a new `Build` by pulling repository and building a Docker image
3. The Docker image is pushed to an `ImageStream`
4. The `ImageStream` notifies a `Deployment` that a new image is available
5. The `Deployment` spins up a new `Pod` (Container) based on the image
6. Once the new `Pod` is available, it turns off the old `Pod` running the previous version

With **Continuous Deployment**, every change that passes CI and merged to `main` is deployed to production and live, allowing teams to **ship updates faster, reduce the risk of large releases, and catch issues early**.  

## CI/CD Demo Pipeline Tutorial

In the next tutorial, you’ll configure a full **CI/CD pipeline** for a sample repository, using **GitHub Actions for CI and Kubernetes (via OKD) for CD**. Get ready to see automation in action!

### Cloning the Starter Repository

Individually, accept the following GitHub Classroom assignment: <https://classroom.github.com/a/7izSQo1P>

Then, on your host machine outside of any other project, clone your repository. Open this repository in VSCode and then open it in a VS Code Dev Container.

If you are on Windows and the build fails, open `.devcontainer/post-create.sh` and check the line ending setting for this file. It needs to be `LF` not `CRLF`. If you see `CRLF` in the bottom right of the screen, click it, select `LF` and then save the file and rebuild the container.

Before continuing, a few things to open and check out:

1. In the `.devcontainer/devcontainer.json` the `postCreateCommand` runs the `bash` script named `post-create.sh`
2. In the `.devcontainer/post-create.sh` script, you will notice the first set of steps "Installs the `oc` CLI tool." This `oc` tool is what we will use to communicate with your production setup in the cloud. This script also installs our Python packages from `requirements.txt`
3. Open a new terminal in VSCode and run `pytest` to see that tests pass.
4. Open up `main.py` to see that this app simply produces the current times in two timezones. You can try running the app locally with `fastapi dev --reload`. Navigate to the root URL and `/docs` to see the app in question is _very_ simple.

Now you are ready to setup continuous integration and continuous deployment!

### Continuous Integration Demo

Continuous Integration is controlled by a GitHub Action. Since our project's test are written in Pytest, we want the CI system to run `pytest` as part of its workflow. We've already set you up well for this, normally you'd have to create the following directory structure and `yml` file, but for your part to get this going you need to:

1. Open `.github/workflows/test.yml`
2. Read the names of each step to see how the worklflow builds up
3. Find the commented lines:
    ~~~
    - name: Test with pytest (CI)
        run: pytest
    ~~~
4. Uncomment those lines.

Save the file then **make a git commit, on `main`, with these changes**. Then, **push your changes to `origin`.**. For this tutorial, to keep the focus on what's important, we will make all commits and pushes to `main`. In a full industrial CI/CD pipeline, you would take this further and be sure pushes are only happening on branches and merged in to `main`, following CI success, via pull requests.

Now, go open the repository you just setup and pushed to in your web browser on GitHub. Look for the Actions tab. Click it and look to see the most recent workflow run. It may still be running or have finished with a green check. Click it. Click through to `test`. Then take a look at the steps of this workflow looking specifically for `Test with pytest (CI)`. Expand that step. Here you can see the 3 tests passed! GitHub actions ran your tests on their machines as part of this CI process. Since everything passed, `pytest`'s process exited with status code 0, and GitHub Actions uses that as a signal that your CI workflow succeeded. Once it does, and any steps following succeed, you will see a green check!

If you navigate back to the "Code" tab in GitHub, then you will also see a small green check just above your list of files, following your commit message. Click it and you can see this check is part of the indication that continuous integration succeeded thanks to our "Run Python Tests" workflow succeeding. (Notice: that _name_ came from the name we gave the workflow at the top of the `test.yml` action specification.)

### Continuous Deployment Demo

Setting up deployment takes some more effort because we need to stand up a production cloud environment. Our production environment will be UNC Cloud Apps' "OKD" cluster, set up just for our course!

**You need to be connected to Eduroam, or connected to [UNC VPN (instructions here)](https://ccinfo.unc.edu/start-here/secure-access-on-and-off-campus/), in order to successfully use OKD. If you are on a home network, UNC guest, or other network, be sure to connect via VPN.**

Login to `OKD` by going to: <https://console.apps.unc.edu>

(If your login does not succeed, it's likely because you did not previously register for Cloud Apps. You can do so by going to https://cloudapps.unc.edu/ and following the Sign Up steps. It can take up to 15 minutes following Sign Up for the OKD link above to work correctly. In the interim, feel free to follow along with your neighbor.)

Once logged in you sould see **OKD** in the upper-left corner. If you see "Red Hat", be sure you opened the link above.

Now that you are logged in, go to the upper-right corner and click your ONYEN and go to the "Copy Login Command" link. Click Display Token. In this, copy the command in the first text box. Paste it into your dev container's terminal (which has the `oc` command-line application for interfacing with a Red Hat Open-Shift Kubernetes cluster installed).

Before proceeding, switch to your personal OKD project using your ONYEN. For example, if your ONYEN is "jdoe", run:
```bash
oc project comp590-140-25sp-jdoe
```

If the above command fails, restart the steps above! The following will not work until you are able to access your project via `oc`.

## Deploying to OKD using CI/CD (Integrated DeploymentConfig)

This guide shows you how to deploy this FastAPI project to OKD following a successful CI/CD test run using an integrated DeploymentConfig that includes its own BuildConfig and ImageStream. In this setup, after tests pass in GitHub Actions, the build is automatically triggered on OKD. The BuildConfig uses the `Dockerfile` from the repository, and the resulting image is deployed automatically with the app name set to `comp423-cicd-demo`.

### 1. Generating a Personal Access Token for Your Private Repository

OKD needs to be able to clone your private repository from GitHub. In order to do so, you will generate a Personal Access Token (legacy) and configure your OKD project to use this access token.

Follow these steps to create a Personal Access Token (PAT) with read access for your repository:

1. **Sign in to GitHub**  
    - Go to [GitHub](https://github.com) and log in with your account.

2. **Navigate to Developer Settings**  
    - Click on your profile picture (top-right corner) and select **Settings**.
    - In the left sidebar, click on **Developer settings**.

3. **Access Personal Access Tokens**  
    - Click on **Personal access tokens**.
    - Select **Tokens (classic)**.

4. **Generate a New Token**  
    - Click the **"Generate new token"** button.
    - For classic tokens, click **"Generate new token (classic)"**.
    - Provide a descriptive name for the token (e.g., "OKD-Repo-ReadAccess").

5. **Select the Scope**  
    - Under **"Select scopes"**, check the **`repo`** scope.
   
6. **Generate and Copy the Token**  
    - Click **"Generate token"**.
    - **Copy the generated token to your clipboard immediately.** You won't be able to see it again later.

### 2. Register your GitHub PAT with a Secret Stored in OKD

From the built-in terminal in your dev container:

1. **Create a GitHub access secret**  
   Create a secret in OKD that contains your GitHub username and a personal access token (PAT) with appropriate repo rights. Remove the surrounding less than and greater than signs when substituting your personal GitHub username and PAT in the command below:
   ```bash
   oc create secret generic comp423-cicd-git-credentials \
       --from-literal=username=<your-github-username> \
       --from-literal=password=<your-github-pat> \
       --type=kubernetes.io/basic-auth
   ```
2. **Label the Secret**  
   Add the label "app=comp423-cicd-demo" to make it easier to delete everything related to this demo later on:
   ```bash
   oc label secret comp423-cicd-git-credentials app=comp423-cicd-demo
   ```

### 3. Create an Integrated Deployment (with BuildConfig, ImageStream, and Source Secret)

OKD's `new-app` command is a handy all-in-one command to create an application from a repository that handles setting up the app's `BuildConfig`, `ImageStream`, and `Deployment` behind the scenes.

```bash
oc new-app . \
--name=comp423-cicd-demo \
--source-secret=comp423-cicd-git-credentials \
--strategy=docker \
--labels=app=comp423-cicd-demo
```

*Explanation*:  

* The `--source-secret=comp423-cicd-git-credentials` flag directs OKD to use the secret you created to clone the private repo.
* The `--labels=app=comp423-cicd-demo` parameter tags the created BuildConfig, ImageStream, and DeploymentConfig with a common label, "app=comp423-cicd-demo".

Over in OKD, in the web browser, you should look to see the application appear in your project. You should find its build status and track the build.

### 4. Expose the Service

Your OKD pods are securely only accessible to you, or other users you give access to, and not the general public. To begin the process of exposing a pod to the public, we need to expose a route to it in OKD. The following `create route` will automatically generate a route URL securely connecting your service to the outside world:

```bash
oc create route edge --service=comp423-cicd-demo
```

Routes can also be created with custom hostnames, but the automatic name is sufficient for this tutorial.

After doing so, **once your project successfully builds**, you can run the following command:

```bash
oc get route comp423-cicd-demo
```

What this will do is show you the public route to your app running in production. Try opening this URL in your browser or your phone. This is live on the public internet!

### 5. Setting up Continuous Deployment Using a Webhook Callback from GitHub Actions to OKD

A webhook callback is a mechanism by which OKD can be triggered to start a new build when it receives an HTTP POST request. In this setup, after your tests pass on GitHub Actions, a POST request is sent to the webhook URL configured in your OKD BuildConfig. This webhook URL contains a secret token that ensures only authorized calls (i.e. from your GitHub Actions) can trigger a build. 

To configure this:

1. To get the webhook URL:
   ```bash
   oc describe bc/comp423-cicd-demo | grep -C 1 generic
   ```
2. To get the webhook secret token:
   ```bash
   oc get bc comp423-cicd-demo -o yaml | grep -C 1 generic
   ```
   Look for the "generic" trigger section and note the secret token.
3. In your GitHub repository, add this full URL as a secret named `WEBHOOK_URL`:
   - Go to **Settings > Security > Secrets and Variables > Actions > Repository Secrets > New Repository Secret**.
   - Set the name to `WEBHOOK_URL` and paste in the full URL. The full URL is comprised of the URL template found in the command above and substituting the secret into the path. This secret in your repository is what will be referenced in the next GitHub Action variable. Note: **you will ==NOT== put the URL directly into the action definition!**
4. In your GitHub Actions workflow, uncomment the following step to use `curl` to send a POST request to trigger a new build:
    {% raw %}
   ```yaml
   - name: Trigger OKD Build via Webhook
     if: success()
     run: |
       curl -X POST "${{ secrets.WEBHOOK_URL }}"
   ```
    {% endraw %}
   This step uses the webhook URL to trigger a build only when prior steps succeed, thanks to the `if` condition where `success()` is established by the workflow steps prior.

You can try testing this by modifying something simple in your application that will not break the tests. For example, perhaps just switch the ordering in `main.py` of the two timezones in the `TIMEZONES` constant. Make a commit with the changes to your app and `test.yml`. Push the commit to `main` (we can circumvent best practices about branching for educational purposes here!) When you open your GitHub repository, you can see the action flow through the steps. In one of the final steps you will see "Deploy to production". If you then go look at OKD, you will see a new build is kicked off and working to build a new production image. Once it completes, the image is deployed to your app and it is live on the web! This is continuous integration (via testing) and continuous deployment (contingent on tests passing)! These flows are common in industrial software engineering settings.

## Summary

This setup allows a robust CI/CD pipeline where any push or PR to the main branch runs tests via GitHub Actions. After successful tests, a secure webhook callback is sent to OKD to start a build. The configuration ensures the Dockerfile (from the ".production" directory) is used and the application (tagged with "app=comp423-cicd-demo") is deployed with minimal manual intervention, while keeping sensitive tokens secure within GitHub Secrets.

Happy deploying!

---

## Cleaning Up CI/CD Demo Components on OKD

When you're ready to clean up all the components created by this deployment, you can delete them all in one step by using the label selector:

```bash
oc delete all -l app=comp423-cicd-demo
oc delete secret -l app=comp423-cicd-demo
```

These commands will remove all resources (Deployment, BuildConfig, ImageStream, Service, Route, and secrets) tagged with "app=comp423-cicd-demo" while leaving your OKD project intact for future work.

