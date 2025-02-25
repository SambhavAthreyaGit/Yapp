import json
import anthropic
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def generate_cuts(transcription):
    # Get the API key from the environment variable
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env file")

    client = anthropic.Client(api_key=api_key)

    # Prepare the prompt for Claude
    prompt = f"""
Human: Analyze the following transcript and identify parts that can be cut without ruining the flow of the script. Focus on removing filler words, remove uncessary fluff and parts of a sentence that won't disrupt the flow,repetitions, and unnecessary pauses while maintaining the core message and natural flow of speech. Ensure cuts are at least 0.5 seconds long, consider context, prioritize cutting filler words and pauses, and avoid cutting important information.

Transcript with word-level timestamps:
{json.dumps(transcription['segments'], indent=2)}

Provide the cuts in this JSON format:
{{
    "cuts": [
        {{
            "start_time": float,
            "end_time": float,
            "text_that_is_cut": "string"
        }}
    ]
}}

Assistant: Based on the provided transcript, here are the suggested cuts:
"""

    # Get Claude's response
    response = client.completions.create(
        model="claude-2.1",
        prompt=prompt,
        max_tokens_to_sample=2000
    )

    try:
        # Extract the JSON part from the response
        json_start = response.completion.find("{")
        json_end = response.completion.rfind("}") + 1
        if json_start == -1 or json_end == -1:
            raise ValueError("JSON part not found in API response")

        json_response = response.completion[json_start:json_end]

        # Parse the JSON response
        cuts = json.loads(json_response)

        # Post-process cuts to ensure minimum duration
        min_duration = 0.5
        cuts['cuts'] = [cut for cut in cuts['cuts'] if cut['end_time'] - cut['start_time'] >= min_duration]

        with open("cuts.json", "w") as f:
            json.dump(cuts, f, indent=2)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print("Response content that caused the error:")
        print(response.completion)
        raise

    return cuts
