FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ssh-client \
    software-properties-common \
    make \
    build-essential \
    ca-certificates \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir dbt-core dbt-snowflake

# Set working directory
WORKDIR /dbt

# Copy dbt project
COPY . /dbt

# The command to run when the container starts
CMD ["dbt", "run"]