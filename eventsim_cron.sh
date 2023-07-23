#!/bin/bash

# current_directory=

# echo $pwd

# # Add a new cron job entry
(crontab -l 2>/dev/null; echo "*/15 * * * * $(pwd)/eventsim_producer.sh >> $(pwd)/eventsim.log") | crontab -

# # List existing cron jobs
crontab -l