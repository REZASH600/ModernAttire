# Define the Python version to use for the base image
ARG PYTHON_VERSION=3.11.2-bullseye

# Set up the base image with the specified Python version
FROM python:${PYTHON_VERSION} AS python

# Create a build stage for preparing dependencies
FROM python AS python-build-stage

# Update package lists and install necessary build tools and libraries
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \  
    libpq-dev           

# Copy the requirements file to the build context
COPY ./requirements .

# Build wheels for the required Python packages to speed up installation
RUN pip wheel --wheel-dir /usr/src/app/wheels \
  -r local.txt

# Create the final stage for running the application
FROM python AS python-run-stage

# Define the application's home directory inside the container
ARG APP_HOME=/app

# Disable writing .pyc files (Python bytecode) to improve container performance
ENV PYTHONDONTWRITEBYTECODE=1

# Disable Python output buffering to improve log visibility in Docker
ENV PYTHONUNBUFFERED=1

# Set the working directory for the application
WORKDIR ${APP_HOME}

# Update package lists and install necessary runtime libraries, then clean up
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \           
    gettext \             
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*  

# Copy the built wheels from the build stage to the current stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Install dependencies from the pre-built wheels without accessing the internet
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/    

# Copy the startup script to the container and prepare it for execution
COPY ./docker/local/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh   
RUN chmod +x /start.sh           

# Copy the core application code into the container
COPY ./core ${APP_HOME}

