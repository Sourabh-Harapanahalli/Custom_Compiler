#!/bin/bash

REPO_URL="https://github.com/sourabh-harapanahalli/DLang-Compiler-Project.git"
COMMIT_MESSAGE=${1:-"Automated commit"}

# Navigate to the project directory
cd "$(dirname "$0")"

# Initialize Git (if not already initialized)
if [ ! -d .git ]; then
    git init
    git remote add origin $REPO_URL
fi

# Add changes
git add .

# Commit changes
git commit -m "$COMMIT_MESSAGE"

# Push changes
git push -u origin main
