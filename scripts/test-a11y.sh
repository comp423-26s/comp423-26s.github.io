#!/bin/bash
set -e

# Function to cleanup background process
cleanup() {
    if [ -n "$MKDOCS_PID" ]; then
        echo "Stopping MkDocs server..."
        kill $MKDOCS_PID
    fi
}

# Trap exit to ensure cleanup
trap cleanup EXIT

# Check if MkDocs is already running
if curl -s http://127.0.0.1:8000 > /dev/null; then
    echo "MkDocs server is already running."
else
    echo "Starting MkDocs server..."
    mkdocs serve &
    MKDOCS_PID=$!
    
    echo "Waiting for server to be ready..."
    # Wait up to 30 seconds
    for i in {1..30}; do
        if curl -s http://127.0.0.1:8000 > /dev/null; then
            echo "Server is ready."
            break
        fi
        sleep 1
    done
    
    if ! curl -s http://127.0.0.1:8000 > /dev/null; then
        echo "Failed to start MkDocs server."
        exit 1
    fi
fi

echo "Running pa11y-ci..."
pa11y-ci --sitemap http://127.0.0.1:8000/sitemap.xml
