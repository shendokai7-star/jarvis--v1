import pyttsx3
import requests
from bs4 import BeautifulSoup
import time

# window based
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

import requests

def get_temperature():
    api_key = "fe450cc3a684cd6d9f6b7640685e2099"
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Assam&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        return f"The temperature is {temp} degrees Celsius."
    else:
        return "Sorry, I couldn't find the temperature for Assam."

def Temper():
    Speak(get_temperature())
    

