import pyttsx3

def Speak(text, rate=195):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    zira_voice_id = None
    for voice in voices:
        if "Zira" in voice.name:
            zira_voice_id = voice.id
            break
    if zira_voice_id:
        engine.setProperty('voice', zira_voice_id)
    else:
        print("Zira voice not found.")
    
    engine.setProperty('rate', rate)  # Adjust the speech rate (words per minute)
    engine.setProperty('volume', 1.0)  # Set the speech volume (0.0 to 1.0)
    engine.setProperty('pitch', 0)  # Set the speech pitch (0 to 100)

    print("")
    print(f" AI: {text}")
    print("")
    
    engine.say(text)
    engine.runAndWait()

# Example usage:
