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