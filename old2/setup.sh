#!/bin/bash

export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
export LANGCHAIN_API_KEY="your-api-key"
export LANGCHAIN_PROJECT="rika-bot"
export GOOGLE_API_KEY="your-google-api-key"
export DISCORD_TOKEN="your-discord-token"

# Setup For server
./.venv/bin/python3 ./src/main.py