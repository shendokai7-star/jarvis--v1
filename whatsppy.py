from time import sleep
from Body.listen import MicExecution
import webbrowser
from Body.speak2 import Speak
import pyautogui

ListWeb = {'brother': "+919395293936",
           'dost': "+919876543210",
           'pote': '+911234567890'}

def WhatsappSender(Name):
    if Name not in ListWeb:
        print("Invalid Name")
        return
    Speak(f"Preparing To Send a Message To {Name}")
    Speak("What's The Message By The Way?")
    Message =MicExecution()
    Number = ListWeb[Name]
    link = f"https://web.whatsapp.com/send?phone={Number}&text={Message}"
    webbrowser.open(link)
    sleep(7)
    try:
        pyautogui.press('enter')
        Speak("Message Sent")
        sleep(5)
        pyautogui.hotkey("ctrl", "w")
        
    except:
        print("Failed to send message")


