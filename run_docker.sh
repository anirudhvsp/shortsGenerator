#!/bin/bash

# Usage: ./run_docker.sh <ELEVENLABS_API_KEY> <GEMINI_API_KEY> <number_of_iterations> <output_directory>

ELEVENLABS_API_KEY=$1
GEMINI_API_KEY=$2
ITERATIONS=${3:-1} # Default to 1 iteration if not provided
OUTPUT_DIR=${4:-$(pwd)/outputs} # Default to ./outputs if not provided

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

docker build -t ccsg-generator .
docker run --rm \
  -e ELEVENLABS_API_KEY=$ELEVENLABS_API_KEY \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  -v "$OUTPUT_DIR:/app/outputs" \
  ccsg-generator python fullWorkflow.py $ITERATIONS
