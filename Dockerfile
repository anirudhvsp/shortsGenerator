# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy only necessary files (e.g., scripts and requirements)
COPY downloadVideo.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the download script to fetch MC_PARKOUR.mp4
RUN python downloadVideo.py

# Ensure FFmpeg is installed
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Ensure the outputs directory exists
RUN mkdir -p /app/outputs

# Install google-genai library
RUN pip install google-genai

# Install a compatible version of Pillow

# Copy the fullWorkflow.py script into the container
COPY *.py /app/

RUN pip install "Pillow>=9.1.0"

# Default command to run the batch generation script
CMD ["python", "fullWorkflow.py", "1"]