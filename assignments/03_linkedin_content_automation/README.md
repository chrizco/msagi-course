# LinkedIn Content Automation

AI-powered LinkedIn content automation using FastAPI, OpenAI, AutoGen-style agents, n8n, Docker Compose, email approval, and persistent logging.

The project generates professional LinkedIn content while retaining human oversight. Real LinkedIn publishing is currently disabled.

## Architecture

```text
Manual Trigger / Schedule Trigger
                ↓
          Brand Config
                ↓
     AutoGen Microservice
                ↓
          Compose Final
                ↓
          Approval Gate
          /             \
 Human review        Publishing branch
      ↓                  ↓
 Email Approval       Disabled placeholder
      ↓
 Approval Result
   /          \
Approved    Rejected
   ↓            ↓
Log Approved  Log Rejected
```

Docker Compose runs two containers:

```text
linkedin-api
    FastAPI
    OpenAI API
    AutoGen-style agents

n8n
    workflow orchestration
    approval routing
    email approval
    persistent logging
```

Both containers communicate through the Docker Compose network.

## Agent roles

The FastAPI microservice uses four separate AI roles:

1. **Idea Agent**  
   Generates three LinkedIn post concepts.

2. **Draft Agent**  
   Turns the selected idea into a complete LinkedIn post.

3. **Hashtag Agent**  
   Generates five relevant hashtags.

4. **Confidence Agent**  
   Evaluates the draft and returns a confidence score and explanation.

The orchestrator runs these agents sequentially and combines their outputs into one JSON response.

## Project structure

```text
03_linkedin_content_automation/
│
├── app/
│   ├── __init__.py
│   ├── agents.py
│   ├── main.py
│   └── orchestrator.py
│
├── docs/
│   ├── content_log_evidence.png
│   ├── email_approval_success.png
│   ├── fastapi_success_response.pdf
│   ├── n8n_workflow_overview.png
│   └── project_reflection.md
│
├── n8n/
│   └── linkedin_content_automation.json
│
├── notebooks/
│   └── 01_setup_and_api_basics.ipynb
│
├── tests/
│   └── test_api.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── compose.yaml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Requirements

Install:

- Git
- VS Code
- Docker Desktop
- WSL 2 as the Docker backend
- Python 3.13 or another compatible Python version

A separate Ubuntu VM is not required for the local Docker-based implementation.

## Environment setup

Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the Python packages:

```powershell
python -m pip install -r requirements.txt
```

For the learning notebook and tests, also install:

```powershell
python -m pip install jupyter ipykernel pytest httpx
```

Register the Jupyter kernel:

```powershell
python -m ipykernel install --user --name msagi-linkedin --display-name "Python (MSAGI LinkedIn)"
```

## OpenAI configuration

Copy:

```text
.env.example
```

to:

```text
.env
```

Add the real OpenAI API key:

```text
OPENAI_API_KEY=your-real-api-key
```

The `.env` file is excluded from Git and Docker image contents.

Never commit the real API key.

## Start the project

Make sure Docker Desktop is open and its engine is running.

Start both containers:

```powershell
docker compose up --build -d
```

Check their status:

```powershell
docker compose ps
```

Expected services:

```text
linkedin-api
n8n
```

## Open the applications

FastAPI documentation:

```text
http://localhost:8000/docs
```

n8n:

```text
http://localhost:5678
```

## Stop the project

```powershell
docker compose down
```

The n8n workflows, credentials, user account, and data tables remain stored in the persistent Docker volume.

Restart later with:

```powershell
docker compose up -d
```

## FastAPI endpoint

The primary endpoint is:

```text
POST /linkedin
```

Example request:

```json
{
  "company_name": "FinEdge Mumbai",
  "industry": "Fintech",
  "target_audience": "Finance leaders and fintech professionals",
  "topic": "AI engineering challenges in fintech and how to overcome them",
  "tone": "Professional, clear, and lightly humorous",
  "goal": "Build thought leadership and encourage discussion"
}
```

Example response structure:

```json
{
  "ideas": [
    "Idea 1",
    "Idea 2",
    "Idea 3"
  ],
  "selected_idea": "Idea 1",
  "draft": "Generated LinkedIn post",
  "confidence": 0.88,
  "reason": "Quality evaluation",
  "hashtags": [
    "#FintechAI",
    "#MLOps",
    "#ArtificialIntelligence"
  ]
}
```

## n8n workflow setup

Import:

```text
n8n/linkedin_content_automation.json
```

The workflow contains:

- Manual Trigger
- Schedule Trigger
- Brand Config
- AutoGen Microservice
- Compose Final
- Approval Gate
- Email Approval
- Approval Result
- Log Approved
- Log Rejected
- LinkedIn Publishing Disabled

Inside Docker, n8n calls FastAPI using:

```text
http://linkedin-api:8000/linkedin
```

`linkedin-api` is the Docker Compose service name.

Using `localhost` inside the n8n container would incorrectly point back to the n8n container itself.

## Email approval

The workflow currently uses Gmail SMTP for approval emails.

The Gmail credential requires:

```text
Host: smtp.gmail.com
Port: 465
SSL/TLS: enabled
User: Gmail address
Password: Google App Password
```

The Google App Password is not the n8n login password.

The approval email pauses the workflow until the recipient selects:

- Approve
- Disapprove

The result is returned in this structure:

```json
{
  "data": {
    "approved": true,
    "respondedAt": "timestamp"
  }
}
```

## Approval rules

The workflow uses:

```text
minimum_confidence = 0.8
dry_run = true
```

A draft is sent for human review when:

```text
dry_run is true
OR
confidence is below minimum_confidence
```

Only this combination could reach the future publishing route:

```text
dry_run is false
AND
confidence is equal to or above minimum_confidence
```

The publishing route currently ends in a disabled placeholder.

## Logging

Approved and rejected drafts are stored in the n8n Data Table:

```text
LinkedIn Content Log
```

Stored fields:

- timestamp
- topic
- final post
- confidence
- approved
- dry-run status

## Run the tests

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run:

```powershell
python -m pytest
```

Expected result:

```text
1 passed
```

The automated test checks that the FastAPI root endpoint returns HTTP status `200` and the expected response.

## Evidence

Submission evidence is stored in `docs/`:

- complete n8n workflow
- successful FastAPI response
- email approval
- approved and rejected logging
- project reflection

## Troubleshooting

### Docker command not found

Restart Windows or reopen VS Code after installing Docker Desktop.

### Docker build cannot connect to the engine

Open Docker Desktop and wait until it shows:

```text
Engine running
```

### Windows path-length error during Jupyter installation

Enable Windows long-path support and restart Windows.

### FastAPI returns HTTP 422

Check that the request body is valid JSON.

JSON does not allow a trailing comma before the closing brace.

### n8n cannot reach FastAPI

Use:

```text
http://linkedin-api:8000/linkedin
```

Do not use `localhost` from inside the n8n container.

### Forgotten n8n password

Reset local n8n user management:

```powershell
docker compose exec n8n n8n user-management:reset
```

Then create a new owner password and save it securely.

## Safety

Real LinkedIn publishing is disabled.

The workflow currently uses:

```text
dry_run = true
```

No content can be published through the current workflow.

A possible LinkedIn integration will be evaluated separately using a LinkedIn developer application, OAuth authorization, and the required posting permissions.