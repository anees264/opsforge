#!/bin/zsh

# Script to clone multiple git repositories
# Usage: ./clone_repos.sh <repos_file> [output_directory]

REPOS_FILE="${1:-.}"
OUTPUT_DIR="${2:-.}"

# Check if repos file exists
if [[ ! -f "$REPOS_FILE" ]]; then
    echo "Error: Repos file '$REPOS_FILE' not found"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR" || exit 1

echo "Cloning repositories from $REPOS_FILE..."
echo "Output directory: $(pwd)"
echo ""

# Counter for tracking progress
total=$(wc -l < "$REPOS_FILE")
count=0

# Read each repo URL from the file
while IFS= read -r repo_url; do
    # Skip empty lines and comments
    [[ -z "$repo_url" || "$repo_url" =~ ^# ]] && continue
    
    count=$((count + 1))
    echo "[$count/$total] Cloning: $repo_url"
    
    # Extract repo name for error reporting
    repo_name=$(basename "$repo_url" .git)
    
    # Clone the repository
    if git clone "$repo_url"; then
        echo "✓ Successfully cloned $repo_name"
    else
        echo "✗ Failed to clone $repo_url"
    fi
    
    echo ""
done < "$REPOS_FILE"

echo "Done! Cloned $count repositories."