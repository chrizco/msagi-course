# Project Reflection

## Design decisions

The solution separates content generation from workflow orchestration.

The FastAPI microservice handles the AI-related work:

- generating post ideas
- selecting an idea
- drafting the post
- generating hashtags
- evaluating confidence

n8n handles the business workflow:

- preparing the brand configuration
- calling the microservice
- composing the final post
- applying the approval rules
- sending the approval email
- logging approved and rejected drafts
- preparing a future LinkedIn publishing branch

Docker Compose runs FastAPI and n8n as separate containers. This keeps their dependencies isolated while allowing both services to communicate through the shared Docker network.

## Human oversight and safety

The workflow uses a human approval step before any content could be published.

During development:

```text
dry_run = true
```

The future LinkedIn branch is present but ends in a disabled placeholder. Therefore, the workflow cannot currently publish content to LinkedIn.

A minimum confidence threshold provides an additional guardrail. Drafts are sent for review when dry-run mode is enabled or the confidence score is below the threshold.

## Challenges and solutions

### Windows path-length limitation

Installing Jupyter initially failed because some package paths exceeded the default Windows path-length limit.

The Windows long-path setting was enabled, after which the installation succeeded.

### Docker engine not running

The first Docker image build failed because Docker Desktop was closed.

Opening Docker Desktop and waiting for the engine to start resolved the issue.

### Container networking

Inside the n8n container, `localhost` would refer to n8n itself rather than the FastAPI container.

The HTTP Request node therefore calls:

```text
http://linkedin-api:8000/linkedin
```

`linkedin-api` is the Docker Compose service name.

### Invalid JSON request

One FastAPI test returned HTTP 422 because the request body contained a trailing comma.

Removing the final comma produced valid JSON and resolved the issue.

### n8n password recovery

The local n8n installation was not configured with system-wide email recovery.

The owner account was reset through the n8n command-line tool, and a new password was created. Workflow data remained available because it was stored in the persistent Docker volume.

## Trade-offs

The project uses an AutoGen-style architecture rather than the full AutoGen framework. This keeps the implementation understandable while still demonstrating separate agent roles and orchestration.

Email was selected instead of Slack because it provides a valid approval channel without requiring a Slack workspace.

Real LinkedIn publishing was deliberately excluded from the working workflow. Activating it would require a LinkedIn developer application, OAuth authorization, and posting permissions for a real LinkedIn account.

The AI agents currently run sequentially. This is simple and transparent, although it results in several separate OpenAI API calls.

## Learning outcomes

The project provided practical experience with:

- Python functions and dictionaries
- Jupyter notebooks
- OpenAI API calls
- structured JSON
- FastAPI endpoints
- automated tests
- Docker images and containers
- Docker Compose
- container networking
- n8n workflow design
- email approval
- persistent logging
- Git and GitHub

The final solution demonstrates a complete local workflow while retaining human oversight and preventing accidental LinkedIn publishing.