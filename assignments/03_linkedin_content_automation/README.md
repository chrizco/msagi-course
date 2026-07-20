# LinkedIn Content Automation

AI-powered LinkedIn content generation using:

- FastAPI
- OpenAI
- AutoGen-style agents
- n8n
- Docker Compose
- Email approval
- Persistent n8n logging

## Current workflow

1. n8n starts the workflow.
2. Brand configuration is prepared.
3. FastAPI generates ideas, a draft, hashtags, and a confidence score.
4. n8n composes the final post.
5. An approval email is sent.
6. Approved and rejected drafts are logged.
7. LinkedIn publishing remains disabled during development.

## Start the project

```powershell
docker compose up -d
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

## Run the tests

Activate the Python environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the tests:

```powershell
python -m pytest
```

## Safety

Real LinkedIn publishing is currently disabled.

The n8n workflow uses:

```text
dry_run = true
```

The potential LinkedIn publishing branch currently ends in a disabled placeholder node. No content is posted to LinkedIn.