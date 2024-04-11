#!/bin/bash

# Function to check if perfmon.sh script is already in crontab
check_and_add_perfmon() {
    # Define the cron job pattern to look for
    local cron_job="*/15 * * * * /opt/perfmon/perfmon.sh"

    # Use crontab -l to list existing cron jobs, grep to search for the cron job pattern
    if ! crontab -l | grep -Fq -- "$cron_job"; then
        # If the cron job doesn't exist, add it
        (crontab -l 2>/dev/null; echo "$cron_job") | crontab -
        printf "perfmon.sh job added to crontab.\n"
    else
        printf "perfmon.sh job already exists in crontab. No action taken.\n" >&2
    fi
}

# Main function to encapsulate the script's primary logic
main() {
    check_and_add_perfmon
}

# Execute the main function
main
