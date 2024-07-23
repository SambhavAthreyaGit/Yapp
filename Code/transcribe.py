import whisper
import json

def transcribe_video(video_path):
    # Load the Whisper model
    model = whisper.load_model("base")

    # Transcribe the video
    result = model.transcribe(video_path, word_timestamps=True)

    # Save the transcription with timestamps
    with open("transcription.json", "w") as f:
        json.dump(result, f, indent=2)

    return result
