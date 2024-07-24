from transcribe import transcribe_video
from generate_cuts import generate_cuts
from app import app

'''
def main():
    video_path = "TestVideos/1mintedtalk.mp4"

    # Step 1: Transcribe the video
    transcription = transcribe_video(video_path)
    print("Transcription completed")

    # Step 2: Generate cuts
    cuts = generate_cuts(transcription)
    print("Cuts generated")
'''

if __name__ == "__main__":
    app.run(debug=True)