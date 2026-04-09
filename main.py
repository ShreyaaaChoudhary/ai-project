from app import EmpathyEngine

if __name__ == "__main__":
    engine = EmpathyEngine()
    print("Empathy Engine CLI - Generate expressive speech from text")
    text = input("Enter a sentence: ").strip()
    if not text:
        print("No text entered. Exiting.")
    else:
        result = engine.process(text)
        print("\nDetected Emotion:", result["emotion"])
        print("Intensity:", f"{result['intensity']:.2f}")
        print("Voice Rate:", result["params"]["rate"])
        print("Volume:", result["params"]["volume"])
        print("Audio saved to:", result["audio_path"])
