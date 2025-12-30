import time
import datetime
import pyttsx3

def Speak(Text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voices',voices[0].id)
    engine.setProperty('rate',170)
    print("")
    print(f"You Said :{Text}.")
    print("")
    engine.say(Text)
    engine.runAndWait()


def Time():
 strTime=datetime.datetime.now().strftime("%H:%M")
 Speak(f"the time is {strTime} ")
