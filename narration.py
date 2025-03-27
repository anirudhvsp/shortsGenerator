import os
import requests
from datetime import datetime

# ----- Configuration -----
ELEVENLABS_API_ENDPOINT = "https://api.elevenlabs.io/v1/text-to-speech/nIHefZ8GOsC19mjvAhSN"

def read_story_from_file(file_path):
    """Reads and returns the text content from the given file using UTF-8 encoding."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def generate_narration_audio(text):
    """
    Calls the ElevenLabs API to generate narration audio from the provided text.
    Returns the binary audio content.
    """
    headers = {
        "xi-api-key":  os.environ.get("ELEVENLABS_API_KEY"),
        "Content-Type": "application/json"
    }
    payload = {
        "model_id": "eleven_multilingual_v2",
        "text": text,
         "voice_settings": {
            "speed": 1.00,
            "stability": 0.49,
            "similarity_boost": 0.14,
            "style_boost": 0.38,
            "speaker_boost": True
        }
    }
    
    response = requests.post(ELEVENLABS_API_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return response.content

def save_audio_to_file(audio_data, file_path):
    """Saves the binary audio data to a file."""
    with open(file_path, "wb") as f:
        f.write(audio_data)

if __name__ == "__main__":
    # Prompt user for the path to the story file
    # input_file = input("Enter the path to the story file: ").strip()
    input_file = "story_20250325005104.txt"
    if not os.path.exists(input_file):
        print(f"File '{input_file}' not found.")
        exit(1)
    
    # Read story text from file
    story_text = read_story_from_file(input_file)
    
    try:
        # Generate narration audio from the story text
        audio_data = generate_narration_audio(story_text)
    except Exception as e:
        print("Error generating narration audio:", e)
        exit(1)
    
    # Generate a filename with current timestamp to avoid file conflicts
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    audio_filename = f"narration_{timestamp}.mp3"
    
    # Save the audio file
    save_audio_to_file(audio_data, audio_filename)
    print(f"Narration audio saved to '{audio_filename}'")
