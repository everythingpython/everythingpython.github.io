#!/usr/bin/env bash
set -e

# Check if Hugo is installed
if ! command -v hugo &> /dev/null; then
    echo "Hugo not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if ! command -v brew &> /dev/null; then
            echo "Error: Homebrew is not installed. Install it from https://brew.sh"
            exit 1
        fi
        brew install hugo
    elif [[ "$OSTYPE" == "linux"* ]]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y hugo
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y hugo
        elif command -v snap &> /dev/null; then
            sudo snap install hugo
        else
            echo "Error: Could not detect package manager. Install Hugo manually: https://gohugo.io/installation/"
            exit 1
        fi
    else
        echo "Error: Unsupported OS. Install Hugo manually: https://gohugo.io/installation/"
        exit 1
    fi
fi

# Initialize theme submodule if needed
if [ ! -f "themes/hugo-bearblog/theme.toml" ]; then
    echo "Initializing theme submodule..."
    git submodule update --init --recursive
fi

echo "Starting Hugo dev server..."
hugo server -D
