FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# FROM chooses the Python base image.
# WORKDIR creates the working folder inside the container.
# COPY moves files into the container.
# RUN installs the required packages.
# CMD starts FastAPI when the container runs.