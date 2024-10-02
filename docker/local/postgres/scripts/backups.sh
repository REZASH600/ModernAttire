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

# Inform the user about the backup files
message_info "These are the backups:"

# List the backup files in the specified directory with detailed information
ls -lht "${BACKUP_DIR_PATH}"
