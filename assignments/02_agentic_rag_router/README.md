# Assignment 02 - Agentic RAG Router

This assignment implements a multi-agent Router-Retriever RAG system using CrewAI.

## Goal

The system accepts a natural language question, routes it to the most suitable retrieval path, retrieves relevant context, and returns a grounded answer with trace logging.

The assignment demonstrates how an agentic workflow can combine static PDF knowledge with dynamic web search.

## Architecture

The system contains two main agents:

### Router Agent

The Router Agent analyzes the user question and selects exactly one route:

- `pdf_search` for questions about the provided Transformer paper
- `web_search` for current, external, online, or tool-specific information
- `direct_llm` for general conceptual questions that do not require retrieval

### Retriever Agent

The Retriever Agent receives the original question, selected route, retrieved context, and retrieval metadata.

It then creates the final answer and ends with a short source path.

## Retrieval Tools

### PDF Search

The notebook uses CrewAI's `PDFSearchTool` to search inside the provided Transformer research paper:

- `data/attention_is_all_you_need.pdf`

This is the static, domain-specific source.

### Web Search

The notebook uses `TavilySearchResults` for web search.

This is the dynamic source for external or current information.

The Tavily API key is passed explicitly through `TavilySearchAPIWrapper` because this worked more reliably in the local Jupyter environment.

## Coordination Flow

1. User enters a natural language question.
2. Router Agent classifies the question as `pdf_search`, `web_search`, or `direct_llm`.
3. The selected retrieval path is executed.
4. Retriever Agent receives the retrieved context.
5. Retriever Agent generates the final answer.
6. The workflow writes trace events to `outputs/trace_log.json`.

## Trace Logging

The trace log records:

- timestamp
- workflow step
- acting agent
- input
- output
- metadata such as selected tool and source

The notebook also displays the trace log at the end of the run.

## Challenges and Trade-offs

### Local PDF path handling

CrewAI's `PDFSearchTool` blocked the local PDF path at first. Since this project intentionally searches a local course PDF, the notebook sets `CREWAI_TOOLS_ALLOW_UNSAFE_PATHS=true`.

### Tavily authentication in wrapper

The direct Tavily SDK call worked, while the default wrapper initially returned `401 Unauthorized`. Passing the key explicitly through `TavilySearchAPIWrapper` fixed the issue.

### CrewAI in Jupyter

CrewAI's synchronous `kickoff()` call conflicts with the running Jupyter event loop. The notebook therefore uses `kickoff_async()` and calls the workflow with `await`.

### Beginner-friendly scope

The implementation avoids production-level complexity such as persistent vector databases, authentication layers, monitoring dashboards, or advanced fallback chains.

## How to Run

From the repository root:

```powershell
cd C:\Users\ChristopherCopony\Projekte\MSAGI-COURSE
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\assignments\02_agentic_rag_router\requirements.txt
```

Create a local `.env` file inside `assignments/02_agentic_rag_router/` with:

```text
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Then open and run:

```text
assignments/02_agentic_rag_router/notebooks/agentic_rag_router_retriever.ipynb
```

Use the kernel:

```text
Python (msagi-course)
```

## Main Files

- `data/course_end_project_problem_statement.pdf`
- `data/attention_is_all_you_need.pdf`
- `notebooks/agentic_rag_router_retriever.ipynb`
- `requirements.txt`
- `.env.example`
- `README.md`
