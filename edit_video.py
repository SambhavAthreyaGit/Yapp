from moviepy.editor import VideoFileClip, concatenate_videoclips
import json

def apply_cuts(input_video_path, cuts_json_path, output_video_path):
    # Load the video
    video = VideoFileClip(input_video_path)
    
    # Load the cuts
    with open(cuts_json_path, 'r') as f:
        cuts_data = json.load(f)
    
    # Sort cuts by start time
    cuts = sorted(cuts_data['cuts'], key=lambda x: x['start_time'])
    
    # Create subclips
    subclips = []
    last_end = 0
    for cut in cuts:
        if cut['start_time'] > last_end:
            subclips.append(video.subclip(last_end, cut['start_time']))
        last_end = cut['end_time']
    
    # Add the final subclip if necessary
    if last_end < video.duration:
        subclips.append(video.subclip(last_end, video.duration))
    
    # Concatenate subclips
    final_clip = concatenate_videoclips(subclips)
    
    # Write the result to a file
    final_clip.write_videofile(output_video_path)
    
    # Close the clips
    video.close()
    final_clip.close()

    return output_video_path