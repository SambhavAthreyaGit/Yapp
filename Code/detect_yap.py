import openai


openai.api_key = 'sk-proj-K6JC07bdvTfyh27V9iYeT3BlbkFJlO7vK4oPW8Ily8qrwN6k'

def read_script_from_file(file_path):
    with open(file_path, 'r') as file:
        script = file.read()
    return script

def identify_fluff(script):
    prompt = f"""
    The following is a script of a video. Identify the parts of the script that are unnecessary fluff and can be cut without affecting the flow or main points. Mark these parts with square brackets [ ].

    Script:
    {script}

    Revised Script with Fluff Marked:
    """

    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5
    )

    revised_script = response.choices[0].text.strip()
    return revised_script

def main(script_file_path):
    script = read_script_from_file(script_file_path)
    revised_script = identify_fluff(script)
    return revised_script

# Example usage
script_file_path = "Transcriptions/test_script.txt"
revised_script = main(script_file_path)
print("Revised Script with Fluff Marked:\n", revised_script)
