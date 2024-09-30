#!/bin/bash

execution_number=0
  # Wait time between checks in seconds.

while true; do
  wait_time=2*24*3600
  # Get the current hour
  execution_number=$((execution_number + 1))
  echo "------------------------ Execution: $execution_number --------------------------"
  python3 main.py
  python3 db_process.py
  python3 send_email.py
  echo "------------------------ Finished execution. Wait $wait_time seconds ------------------------"
  sleep $wait_time
done
