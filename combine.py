import os
import subprocess
import random

def get_duration(file_path):
    """
    Uses ffprobe to obtain the duration (in seconds) of the given media file.
    """
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", 
            "-show_entries", "format=duration", 
            "-of", "default=noprint_wrappers=1:nokey=1", 
            file_path
        ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        print(f"Error reading duration for {file_path}")
        return 0

def process_audio_files(video_file):
    # Get the total duration of the video (assumed to be 3 minutes, but we read it dynamically)
    video_duration = get_duration(video_file)
    if video_duration == 0:
        print("Could not get video duration. Exiting.")
        return

    audio_dir = "./outputs/audio"
    output_dir = "./outputs/shortsNew"
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over all mp3 files in the audio directory
    for audio_filename in os.listdir(audio_dir):
        if audio_filename.lower().endswith(".mp3"):
            audio_path = os.path.join(audio_dir, audio_filename)
            audio_duration = get_duration(audio_path)
            if audio_duration == 0:
                print(f"Skipping {audio_filename} due to invalid duration.")
                continue

            # Calculate a random start time within the video where the segment of audio_duration fits
            max_start = video_duration - audio_duration
            start_time = random.uniform(0, max_start) if max_start > 0 else 0

            # Define the output file path, changing the extension to .mp4
            output_filename = os.path.splitext(audio_filename)[0] + ".mp4"
            output_path = os.path.join(output_dir, output_filename)

            # Build the FFmpeg command:
            # - -ss {start_time}: seek to the random starting point in the video.
            # - -t {audio_duration}: extract a segment that matches the audio length.
            # - The filter_complex chain:
            #     1. crop the input video to a vertical segment. The crop uses an expression that assumes:
            #        - The height remains the same (ih)
            #        - The width becomes ih*9/16 (for a 9:16 ratio)
            #        - The crop is centered horizontally.
            #     2. scale the cropped video to 1080x1920.
            command = [
                "ffmpeg",
                "-ss", str(start_time),
                "-t", str(audio_duration),
                "-i", video_file,
                "-i", audio_path,
                "-filter_complex", "[0:v]crop=w=ih*9/16:h=ih:x=(iw-(ih*9/16))/2:y=0,scale=1080:1920[v]",
                "-map", "[v]",
                "-map", "1:a",
                "-c:a", "copy",
                "-shortest",
                output_path
            ]

            print(f"Processing {audio_filename}...")
            subprocess.run(command)
            print(f"Created {output_path}")

if __name__ == "__main__":
    video_file = 'MC_Parkour.mp4'
    if not os.path.isfile(video_file):
        print("The video file does not exist.")
    else:
        process_audio_files(video_file)
