import pyttsx3
import datetime


'''
def Speak(Text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voices',voices[0].id)
    engine.setProperty('rate',175)
    print("")
    print(f"You Said :{Text}.")
    print("")
    engine.say(Text)
    engine.runAndWait()
'''
def Speak(Text):
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
    engine.setProperty('rate', 175)
    print("")
    print(f" AI: {Text}")
    print("")
    engine.say(Text)
    engine.runAndWait()

   
def greetMe():
    hour =int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        Speak("Good Morning,Masterkai")
        Speak("How can i help you")
        
    elif hour >12 and hour<=18:
        Speak("Good Afternoon ,Masterkai")
        Speak("How can i help you")
    
    else:
        Speak("Good Evening,Masterkai")
        Speak("How can i help you")


