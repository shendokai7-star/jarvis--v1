import pyttsx3
import datetime
import os

def Speak(Text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voices',voices[0].id)
    engine.setProperty('rate',160)
    print("")
    print(f"You Said :{Text}.")
    print("")
    engine.say(Text)
    engine.runAndWait()
    
extractedtime = open("Database\Alarmtext.txt","r")
time = extractedtime.read()
Time = str(time)
extractedtime.close()

deletetime = open("Database\Alarmtext.txt","rd")
deletetime.truncate(0)
deletetime.close

def ring(time):
    timeset = str(time)
    timenow = timeset.replace("Jarvis","")
    timenow = timenow.replace("set an alarm","")
    Alarmtime = str(timenow)
    print(Alarmtime)
    while True:
        currenttime = datetime.datetime.now().st