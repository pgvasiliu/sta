#!/bin/bash

# Check if the .ENV_GITHUB_TOKEN file exists
if [ -f "../.ENV_GITHUB_TOKEN" ]; then
  # Load the GitHub token from the file
  export GITHUB_TOKEN=$(cat ../.ENV_GITHUB_TOKEN)
elif [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: GitHub token is not set. Please export your GitHub token as an environment variable or provide it in the .ENV_GITHUB_TOKEN file."
  exit 1
fi

git config user.email "pg.vasiliu@gmail.com"

# Get the current version from the latest Git tag
current_version=$(git describe --tags --abbrev=0)

# Increment the version number (assuming a semantic versioning style)
new_version=$(echo $current_version | awk -F. -v OFS=. '{++$NF; print}')

# Commit changes
git add .
git commit -m "Committing changes for version $new_version on $(date)"

# Create a new tag
git tag -a $new_version -m "Version $new_version"

# Push changes and tags to the remote repository
git push origin main
git push origin --tags

# Create a new release on GitHub (assuming you use GitHub releases)
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN"
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/pgvasiliu/sta/releases \
  -d "{\"tag_name\":\"$new_version\",\"name\":\"Release $new_version\",\"body\":\"Release notes for $new_version\"}" && echo "Release $new_version created successfully."


