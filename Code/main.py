from transcribe import transcribe_video
from generate_cuts import generate_cuts

def main():
    video_path = "TestVideos/How to Vlog.mp4"
    
    # Step 1: Transcribe the video
    transcription = transcribe_video(video_path)
    print("Transcription completed")

    # Step 2: Generate cuts
    cuts = generate_cuts(transcription)
    print("Cuts generated")

    # Here you would add the next steps of your project
    # Such as applying the cuts to the video using MoviePy

if __name__ == "__main__":
    main()