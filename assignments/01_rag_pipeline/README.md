# MSAGI RAG Pipeline Assignment

Course-end project for building a Retrieval-Augmented Generation pipeline using PDF chunking, OpenAI embeddings, FAISS, and LangChain.

## Assignment Scope

- Load 2-3 PDF documents
- Split them into chunks
- Generate embeddings using the OpenAI API
- Store embeddings in a FAISS vectorstore
- Run semantic retrieval queries
- Report total chunks, average chunk size, and sample query output

## Project Structure

- data/raw_pdfs/ - selected PDF dataset
- data/vectorstore/ - generated FAISS vectorstore, if saved
- docs/ - report and dataset manifest
- notebooks/ - executed assignment notebook
- outputs/ - generated outputs or exports
- src/ - optional reusable Python code

## Setup

This assignment uses the shared course-level virtual environment:

C:\Users\ChristopherCopony\Projekte\MSAGI-COURSE\.venv

Install dependencies with:

python -m pip install -r requirements.txt

## API Key

Create a local .env file based on .env.example:

OPENAI_API_KEY=your_openai_api_key_here

Do not commit .env to GitHub.
