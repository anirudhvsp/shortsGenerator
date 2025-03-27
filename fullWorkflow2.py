import os
import random
from datetime import datetime
import story
import narration
from moviepy.editor import VideoFileClip, AudioFileClip

def create_output_dirs():
    """
    Creates the output folder structure:
    outputs/text, outputs/audio, outputs/video.
    """
    base_dir = "outputs"
    subdirs = ["text", "audio", "video"]
    for sub in subdirs:
        os.makedirs(os.path.join(base_dir, sub), exist_ok=True)
    return {name: os.path.join(base_dir, name) for name in subdirs}

def main():
    # Create output directories
    out_dirs = create_output_dirs()

    # Store details for video generation later
    video_tasks = []

    for i in range(10):
        print("iteration", (i + 1))
        
        # Generate a new story and save to outputs/text folder
        story_text = story.generate()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        story_filename = os.path.join(out_dirs["text"], f"story_{timestamp}.txt")
        story.save_story_to_file(story_text, story_filename)
        print(f"Story saved to {story_filename}")

        # Read the story (from the saved file) and generate narration audio
        text_for_narration = narration.read_story_from_file(story_filename)
        try:
            audio_data = narration.generate_narration_audio(text_for_narration)
        except Exception as e:
            print("Error generating narration audio:", e)
            continue

        narration_filename = os.path.join(out_dirs["audio"], f"narration_{timestamp}.mp3")
        narration.save_audio_to_file(audio_data, narration_filename)
        print(f"Narration audio saved to {narration_filename}")

        # Save details for video generation
        video_tasks.append((narration_filename, timestamp))

    # Video Generation - done after all story and narration tasks
    video_path = "MC_Parkour.mp4"
    if not os.path.exists(video_path):
        print(f"Video file '{video_path}' not found.")
        return
    
    video_clip = VideoFileClip(video_path)

    for narration_filename, timestamp in video_tasks:
        # Load the narration audio to determine its duration
        audio_clip = AudioFileClip(narration_filename)
        narration_duration = audio_clip.duration
        print(f"Generating video for narration at {narration_filename}...")

        # Determine a random start time ensuring the clip fits within the video length
        max_start = video_clip.duration - narration_duration
        if max_start <= 0:
            print("The video is shorter than the narration duration.")
            continue
        random_start = random.uniform(0, max_start)
        video_subclip = video_clip.subclip(random_start, random_start + narration_duration)

        # Resize and crop for TikTok vertical format (9:16)
        video_resized = video_subclip.resize(height=1920 / 2)
        video_vertical = video_resized.crop(x_center=video_resized.w / 2, width=1080 / 2)

        # Set the narration as the audio for the video clip
        final_clip = video_vertical.set_audio(audio_clip)

        # Save the final video to outputs/video folder
        final_video_filename = os.path.join(out_dirs["video"], f"tiktok_{timestamp}.mp4")
        final_clip.write_videofile(final_video_filename, codec="libx264", audio_codec="aac", threads=8)
        print(f"Final TikTok video saved to {final_video_filename}")

if __name__ == "__main__":
    main()
