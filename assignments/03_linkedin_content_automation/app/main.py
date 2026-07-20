from fastapi import FastAPI, HTTPException # FastAPI creates the web application and handles routing, request parsing, and response formatting
from pydantic import BaseModel # Pydantic is used for data validation and settings management using Python type annotations; 
# BaseModel defines the structure of the request data and ensures that incoming requests adhere to this structure, such as JSON.

from app.orchestrator import create_linkedin_content


app = FastAPI(
    title="LinkedIn Content Automation API",
)


class LinkedInRequest(BaseModel):
    company_name: str
    industry: str
    target_audience: str
    topic: str
    tone: str
    goal: str

# The @app.get("/") decorator defines a GET endpoint at the root URL ("/") of the API. 
# When a GET request is made to this URL, the root function is called.
@app.get("/") 
def root():
    return {
        "message": "LinkedIn Content Automation API is running"
    }

# The @app.post("/linkedin") decorator defines a POST endpoint at the URL "/linkedin".
# When a POST request is made to this URL, the generate_linkedin_post function is called.
@app.post("/linkedin")
def generate_linkedin_post(request: LinkedInRequest):
    try:
        request_data = request.model_dump() # The request.model_dump() method converts the Pydantic model instance into a dictionary
        return create_linkedin_content(request_data)

    except Exception as error:
        print(f"Content generation failed: {error}")

        # The HTTPException is raised to indicate that an error occurred during the content generation process.
        raise HTTPException(
            status_code=500,
            detail="LinkedIn content generation failed.",
        )