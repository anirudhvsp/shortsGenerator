# Chacha Chaudhary Story Generator

An automated pipeline for producing Chacha Chaudhary short-form videos with AI-generated stories and narration.

## Features

- AI story generation using Google's Gemini API
- Text-to-speech narration using ElevenLabs API
- Automated video creation with background gameplay footage
- Vertical video format optimized for platforms like YouTube Shorts/TikTok

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set the following environment variables:
```
ELEVENLABS_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

3. Ensure FFmpeg is installed and accessible in your system's PATH. You can download it from [FFmpeg.org](https://ffmpeg.org/).

4. Download the required video file:
```bash
python downloadVideo.py
```

## Usage

### Single Story Generation
```bash
python main.py
```

### Batch Generation with Custom Video Processing
```bash
python fullWorkflow.py <number_of_iterations>
```

### Combine Existing Audio with Video
```bash
python combine.py
```

## Docker Usage

### Prebuilt Image

1. Pull the latest Docker image:
```bash
docker pull anirudhvsp/shortsgenerator:latest
```

2. Run the container with your API keys and desired output directory:
```bash
docker run -v <your_output_directory>:/app/outputs \
  -e ELEVENLABS_API_KEY=<your_elevenlabs_api_key> \
  -e GEMINI_API_KEY=<your_gemini_api_key> \
  anirudhvsp/shortsgenerator:latest
```

> **Note:** Replace `<your_output_directory>` with the path to the directory where you want the generated videos to be saved. Replace `<your_elevenlabs_api_key>` and `<your_gemini_api_key>` with your respective API keys.

### Build Locally

If you prefer to build the image locally, follow these steps:

1. Build the Docker image:
```bash
docker build -t ccsg-generator .
```

2. Run the container:
```bash
docker run --rm \
  -e ELEVENLABS_API_KEY=your_key_here \
  -e GEMINI_API_KEY=your_key_here \
  -v /path/to/output/directory:/app/outputs \
  ccsg-generator python fullWorkflow.py <number_of_iterations>
```

Alternatively, use the provided `run_docker.sh` script:
```bash
./run_docker.sh <ELEVENLABS_API_KEY> <GEMINI_API_KEY> <number_of_iterations> <output_directory>
```

> **Note:** Replace `<output_directory>` with the path to the directory where you want the generated videos to be saved. If not specified, the default is `./outputs` in the current directory.

## Modifying story content
The theme of the story can be changed by updating the prompt being sent to the LLM inside the file `story.py`. The simplest way would be to replace Chacha Chaudhary with a character of your choice, or if you know what you're doing, create a new prompt entirely.

## Output Structure

The project creates the following output directories:
- `outputs/text/` - Generated story texts
- `outputs/audio/` - Narration audio files
- `outputs/video/` - Final vertical format videos
- `outputs/shortsNew/` - Additional processed videos

## Dependencies

- Google Gemini API for story generation
- ElevenLabs API for text-to-speech
- MoviePy for video processing
- FFmpeg for media manipulation