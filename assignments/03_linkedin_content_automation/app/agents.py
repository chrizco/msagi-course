import os
import json

from dotenv import load_dotenv
from openai import OpenAI


# Load variables from the local .env file.
load_dotenv()

# Create the OpenAI client.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


## Idea Generation Agent

def generate_ideas(request):
    """Generate three LinkedIn post ideas."""

    prompt = f"""
Create exactly three different LinkedIn post ideas.

Company: {request["company_name"]}
Industry: {request["industry"]}
Target audience: {request["target_audience"]}
Topic: {request["topic"]}
Tone: {request["tone"]}
Goal: {request["goal"]}

Return one idea per line.
Do not add an introduction.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=(
            "You are an Idea Agent specializing in professional "
            "LinkedIn content for fintech companies, while maintaining a conversational, human-like tone."
        ),
        input=prompt,
        store=False,
    )

    ideas = [
        line.strip()
        for line in response.output_text.splitlines()
        if line.strip()
    ]

    return ideas


## Draft Generation Agent

def generate_draft(request, selected_idea):
    """Generate a complete LinkedIn post draft."""

    prompt = f"""
Write a LinkedIn post based on the following information.

Selected idea:
{selected_idea}

Company: {request["company_name"]}
Industry: {request["industry"]}
Target audience: {request["target_audience"]}
Topic: {request["topic"]}
Tone: {request["tone"]}
Goal: {request["goal"]}

Requirements:
- Write approximately 120 to 180 words.
- Use short, readable paragraphs.
- Do not include hashtags yet.
- End with a question that encourages discussion.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=(
            "You are a Draft Agent specializing in professional "
            "LinkedIn posts for fintech companies, while maintaining a conversational, human-like tone."
        ),
        input=prompt,
        store=False,
    )

    return response.output_text.strip()


## Hashtag Generation Agent

def generate_hashtags(request, draft):
    """Generate five relevant LinkedIn hashtags."""

    prompt = f"""
Create exactly five relevant LinkedIn hashtags.

Industry: {request["industry"]}
Topic: {request["topic"]}

LinkedIn post:
{draft}

Requirements:
- Return one hashtag per line.
- Include the # symbol.
- Do not add explanations.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=(
            "You are a Hashtag Agent specializing in professional "
            "LinkedIn content."
        ),
        input=prompt,
        store=False,
    )

    hashtags = [
        line.strip()
        for line in response.output_text.splitlines()
        if line.strip()
    ]

    return hashtags


## Confidence Scoring Agent

def evaluate_draft(request, draft):
    """Evaluate the draft and return a confidence score."""

    prompt = f"""
Review this LinkedIn post.

Target audience: {request["target_audience"]}
Tone: {request["tone"]}
Goal: {request["goal"]}

Post:
{draft}

Return only valid JSON in this exact format:

{{
  "confidence": 0.85,
  "reason": "Short explanation"
}}

The confidence must be between 0.0 and 1.0.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=(
            "You are a quality-control agent for professional LinkedIn content."
        ),
        input=prompt,
        store=False,
    )

    return json.loads(response.output_text)
