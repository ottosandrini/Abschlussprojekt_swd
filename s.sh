#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <add|print>"
  exit 1
fi

action=$1

if [ "$action" == "add" ]; then
  # Git add
  git add --all

  # Ask for commit message
  read -p "Enter commit message: " message

  # Git commit
  git commit -m "$message"

  echo "Changes committed with message: $message"
elif [ "$action" == "print" ]; then
  echo "This program works"
else
  echo "Invalid argument. Usage: $0 <add|print>"
  exit 1
fi

