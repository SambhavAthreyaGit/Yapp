from transcribe import transcribe_video
from generate_cuts import generate_cuts
from app import app

if __name__ == "__main__":
    app.run(debug=True)