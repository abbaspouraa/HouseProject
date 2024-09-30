#!/bin/bash

execution_number=0
  # Wait time between checks in seconds.
  wait_time=1800

while true; do
  # Get the current hour
  current_hour=$(date +%H)

  execution_number=$((execution_number + 1))
  if [ "$current_hour" -ge 19 ] && [ "$current_hour" -le 20 ]; then
    echo "------------------------ Execution: $execution_number --------------------------"
    python3 main.py
    python3 db_process.py
    python3 send_email.py
    echo "------------------------ Finished execution ------------------------"
  fi
  sleep $wait_time
done
