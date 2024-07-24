import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from transcribe import transcribe_video
from generate_cuts import generate_cuts
from edit_video import apply_cuts
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the video
            transcription = transcribe_video(filepath)
            cuts = generate_cuts(transcription)
            
            # Save cuts to a file
            cuts_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'cuts.json')
            with open(cuts_filepath, 'w') as f:
                json.dump(cuts, f)
            
            # Apply cuts to the video
            output_filename = f"edited_{filename}"
            output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            apply_cuts(filepath, cuts_filepath, output_filepath)
            
            return render_template('download.html', filename=output_filename)
    return render_template('uploads.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True)