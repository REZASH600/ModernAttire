#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -o errexit

# Treat unset variables as an error and exit immediately
set -o nounset

# Fail a pipeline if any command in the pipeline fails
set -o pipefail

# Get the directory of the current script
working_dir="$(dirname "${0}")"

# Source utility scripts for constants and messages
source "${working_dir}/utils/constant.sh"
source "${working_dir}/utils/messages.sh"

# Inform the user about the backup process
message_welcome "Backing up the ${POSTGRES_DB} database..."

# Prevent backup if the user is 'postgres'
if [[ "${POSTGRES_USER}" == "postgres" ]]; then
  message_error "Backing up as 'postgres' user is not allowed."
  exit 1
fi

# Set environment variables for PostgreSQL connection
export PGDATABASE="${POSTGRES_DB}"
export PGUSER="${POSTGRES_USER}"
export PGPASSWORD="${POSTGRES_PASSWORD}"
export PGHOST="${POSTGRES_HOST}"
export PGPORT="${POSTGRES_PORT}"

# Create a backup filename with a timestamp
backup_filename="${BACKUP_FILE_PREFIX}_$(date +'%Y_%m_%dT%H_%M_%S').sql.gz"

# Perform the database backup and compress it with gzip
pg_dump | gzip > "${BACKUP_DIR_PATH}/${backup_filename}"

# Notify the user that the backup was successful
message_success "${POSTGRES_DB} database backup ${backup_filename} has been created successfully and placed in ${BACKUP_DIR_PATH}."
