import os
from datetime import datetime
from google import genai
from google.genai import types

def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="Write a story"),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""Create engaging, fast-paced YouTube Shorts scripts inspired by Chacha Chaudhary comics, narrated by a single storyteller. 
The tone should be witty, humorous, and family-friendly, with concise storytelling suitable for 60-second shorts.
Output only include the content within <Story> tags in Hindi and presented in a continuous flow for seamless TTS narration.
Use simple language and include witty remarks. Ensure Sabu plays a supportive but impactful role and add a small challenge or conflict that Chacha Chaudhary resolves cleverly.
Aim for 100-150 words.
Example Story Outline:
<Story>
"एक दिन चाचा चौधरी अपने घर के बाहर बैठे थे। अचानक एक शातिर चोर उनके घर में चोरी करने आया। चाचा चौधरी ने फौरन एक चाल चली। उन्होंने फर्श पर पानी से भरी बाल्टी रख दी। जैसे ही चोर ने घर में कदम रखा, वो फिसलकर बाल्टी में जा गिरा। साबू ने मुस्कुराते हुए कहा, 'इस चोर को तो नहाने की बहुत ज़रूरत थी!' चाचा चौधरी ने हंसते हुए कहा, 'बेटा, अक्ल के सामने चालाकी कभी नहीं टिकती!'"
</Story>"""),
        ],
    )

    # Collect all chunks into one string
    collected_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        collected_text += chunk.text

    # Extract the content within <Story> tags
    start_tag = "<Story>"
    end_tag = "</Story>"
    start_index = collected_text.find(start_tag)
    end_index = collected_text.find(end_tag, start_index)
    if start_index == -1 or end_index == -1:
        raise ValueError("Story tags not found in the generated text.")
    story_text = collected_text[start_index + len(start_tag):end_index].strip()
    return story_text

def save_story_to_file(story_text, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(story_text)

if __name__ == "__main__":
    story = generate()
    # Generate a filename with the current timestamp to avoid conflicts
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = f"story_{timestamp}.txt"
    save_story_to_file(story, file_path)
    print(f"Story saved to {file_path}")
