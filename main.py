import story
import narration
from datetime import datetime

def main():
    # Generate a new story and save it to a file
    story_text = story.generate()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    story_filename = f"story_{timestamp}.txt"
    story.save_story_to_file(story_text, story_filename)
    print(f"Story saved to {story_filename}")

    # Read the saved story from the file for narration generation
    story_text = narration.read_story_from_file(story_filename)
    
    try:
        # Generate narration audio from the story text
        audio_data = narration.generate_narration_audio(story_text)
    except Exception as e:
        print("Error generating narration audio:", e)
        return

    # Save the generated audio to a file with a unique filename
    narration_filename = f"narration_{timestamp}.mp3"
    narration.save_audio_to_file(audio_data, narration_filename)
    print(f"Narration audio saved to '{narration_filename}'")

if __name__ == "__main__":
    main()
