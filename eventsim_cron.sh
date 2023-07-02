#!/bin/bash

# current_directory=

# echo $pwd

# # Add a new cron job entry
(crontab -l 2>/dev/null; echo "2 * * * * $(pwd)/dummy.sh >> output.log") | crontab -

# # List existing cron jobs
crontab -l