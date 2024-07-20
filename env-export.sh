#!/bin/sh

export $(grep -v '^#' .env | xargs)

echo "Environment variables exported from .env file"
