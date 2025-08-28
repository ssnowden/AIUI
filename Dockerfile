# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11

# Environment variables
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
# COPY Pipfile Pipfile.lock /app/
COPY Pipfile /app/
RUN pip install pipenv && pipenv lock && pipenv install  --deploy --system --dev

# Copy the project
COPY . /app/
