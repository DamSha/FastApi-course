# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.7
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN mkdir -p /var/www/app
WORKDIR /var/www/app

# Copy the source code into the container.
COPY pyproject.toml poetry.lock ./

# Update pip
RUN #pip install --upgrade pip

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
 RUN  --mount=type=cache,target=/tmp/.cache/pip \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    pip install --upgrade pip && pip install poetry && poetry install -n --no-root && rm -rf $POETRY_CACHE_DIR

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
#ARG UID=10001
#RUN adduser \
#    --disabled-password \
#    --gecos "" \
#    --home "/nonexistent" \
#    --shell "/sbin/nologin" \
#    --no-create-home \
#    --uid "${UID}" \
#    appuser
#
#RUN chown -R appuser /var/www/app
#
## Switch to the non-privileged user to run the application.
#USER appuser

COPY ./app /var/www/app

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
#CMD fastapi 'dev' 'main_gradio.py'
CMD uvicorn 'main_gradio:app' --host=0.0.0.0 --port=8000 --workers=4
