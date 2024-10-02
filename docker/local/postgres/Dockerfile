# Use the official PostgreSQL 15 image based on Debian Bullseye as the base image
FROM postgres:15-bullseye

# Copy custom scripts from the local directory to the container's scripts directory
COPY ./docker/local/postgres/scripts /usr/local/bin/scripts

# Make all scripts in the scripts directory executable
RUN chmod +x /usr/local/bin/scripts/*

# Move the scripts to the local bin directory and remove the now-empty scripts directory
RUN mv /usr/local/bin/scripts/* /usr/local/bin \
    && rmdir /usr/local/bin/scripts

# Expose the PostgreSQL default port (5432) to allow external connections
EXPOSE 5432
