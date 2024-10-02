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

# Check if a backup file name is provided as an argument
if [[ -z ${1+x} ]]; then
  message_error "Backup file name is not specified yet."
  exit 1
fi

# Construct the full path for the backup file
backup_filename="${BACKUP_DIR_PATH}/${1}"

# Check if the specified backup file exists
if [[ ! -f ${backup_filename} ]]; then
  message_error "No backup file name with specified name was found."
  exit 1
fi

# Inform the user about the restoration process
message_welcome "Restoring the ${POSTGRES_DB} database from ${backup_filename} backup."

# Prevent restoration if the user is 'postgres'
if [[ "${POSTGRES_USER}" == "postgres" ]]; then
  message_error "Restoring as 'postgres' user is not allowed."
  exit 1
fi

# Set environment variables for PostgreSQL connection
export PGDATABASE="${POSTGRES_DB}"
export PGUSER="${POSTGRES_USER}"
export PGPASSWORD="${POSTGRES_PASSWORD}"
export PGHOST="${POSTGRES_HOST}"
export PGPORT="${POSTGRES_PORT}"

# Notify the user about dropping the existing database
message_info "Dropping the database..."

# Drop the existing database
dropdb "${PGDATABASE}"

# Notify the user about creating a new database
message_info "Creating a new database..."

# Create a new database with the specified owner
createdb --owner="${PGUSER}"

# Inform the user about applying the backups to the database
message_info "Applying the backups to the database..."

# Decompress the backup file and pipe the output into the PostgreSQL client for restoration.
gunzip -c "${backup_filename}" | psql "${POSTGRES_DB}"

# Inform the user that the restoration was successful.
message_success "The '${POSTGRES_DB}' database has been restored successfully from '${backup_filename}' backup."
