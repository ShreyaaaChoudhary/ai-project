# Empathy Engine

A simple Python service that detects emotion from text and generates expressive speech by modulating vocal rate and volume.

## What it does
- Accepts text input via a web form or CLI.
- Detects one of three emotions: Positive, Frustrated, Neutral.
- Maps detected emotion to voice parameters (rate and volume).
- Generates a `.wav` audio file with expressive speech.

## Run locally  

1. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

2. Start the web app:
   ```bash
   python app.py
   ```

3. Open your browser at `http://127.0.0.1:5000`

4. Enter text and click **Generate Voice**.

## CLI usage

Run:
```bash
python main.py
```
Enter a sentence when prompted, and the app saves a `.wav` file under `audio_outputs/`.

## Design notes
- `vaderSentiment` classifies sentiment and maps it to three categories.
- `pyttsx3` synthesizes audio locally and can save speech to a `.wav` file.
- The engine changes `rate` and `volume` based on emotion intensity:
  - Positive: faster and louder
  - Frustrated: slower and softer
  - Neutral: balanced delivery

## Files
- `app.py`: Flask service and empathy engine
- `main.py`: CLI entry point
- `templates/index.html`: simple web interface
- `requirements.txt`: dependencies

## Output
Generated audio files are stored in `audio_outputs/`.
