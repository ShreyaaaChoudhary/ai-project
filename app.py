import os
import uuid
from pathlib import Path
from flask import Flask, render_template, request, send_from_directory
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pyttsx3

BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio_outputs"
AUDIO_DIR.mkdir(exist_ok=True)

app = Flask(__name__)

class EmpathyEngine:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def detect_emotion(self, text: str) -> dict:
        scores = self.analyzer.polarity_scores(text)
        compound = scores["compound"]
        if compound >= 0.4:
            label = "Positive"
        elif compound <= -0.3:
            label = "Frustrated"
        else:
            label = "Neutral"

        intensity = min(abs(compound), 1.0)
        return {
            "label": label,
            "compound": compound,
            "intensity": intensity,
            "scores": scores,
        }

    def voice_params(self, emotion_label: str, intensity: float) -> dict:
        if emotion_label == "Positive":
            rate = int(180 + intensity * 80)
            volume = round(0.8 + intensity * 0.2, 2)
        elif emotion_label == "Frustrated":
            rate = int(120 - intensity * 20)
            volume = round(0.7 - intensity * 0.2, 2)
            volume = max(volume, 0.4)
        else:
            rate = 150
            volume = 0.75

        return {
            "rate": rate,
            "volume": volume,
        }

    def synthesize(self, text: str, filename: str, voice_params: dict) -> str:
        output_path = AUDIO_DIR / filename
        engine = pyttsx3.init()
        engine.setProperty("rate", voice_params["rate"])
        engine.setProperty("volume", voice_params["volume"])

        voices = engine.getProperty("voices")
        if voices:
            # Use a second voice if available for variation.
            voice_choice = voices[1].id if len(voices) > 1 else voices[0].id
            engine.setProperty("voice", voice_choice)

        engine.save_to_file(text, str(output_path))
        engine.runAndWait()
        engine.stop()
        return str(output_path)

    def process(self, text: str) -> dict:
        analysis = self.detect_emotion(text)
        params = self.voice_params(analysis["label"], analysis["intensity"])
        audio_filename = f"empathy_{uuid.uuid4().hex}.wav"
        audio_path = self.synthesize(text, audio_filename, params)
        return {
            "text": text,
            "emotion": analysis["label"],
            "intensity": analysis["intensity"],
            "scores": analysis["scores"],
            "params": params,
            "audio_filename": audio_filename,
            "audio_path": audio_path,
        }

engine = EmpathyEngine()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", result=None)

@app.route("/speak", methods=["POST"])
def speak():
    text = request.form.get("text", "").strip()
    if not text:
        return render_template("index.html", result=None, error="Please enter a message.")

    result = engine.process(text)
    audio_url = f"/audio/{result['audio_filename']}"
    return render_template("index.html", result=result, audio_url=audio_url)

@app.route("/audio/<path:filename>")
def audio_file(filename):
    return send_from_directory(str(AUDIO_DIR), filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
