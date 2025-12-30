import os
import webbrowser
import pyautogui
import keyboard
from time import sleep
import pyttsx3
from hon import JarvisAssistant
import re
obj = JarvisAssistant()

def Speak(Text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voices',voices[0].id)
    engine.setProperty('rate',160)
    print("")
    print(f" AI :{Text}.")
    print("")
    engine.say(Text)
    engine.runAndWait()



def Taskcomplier(Query):
    Query = str(Query).lower()
     
    if "start" in Query:
        name_of_web = Query.replace("start", "")
        link = f"https://www.{name_of_web}.com"
        webbrowser.open(link)
        return True
        
    elif "open" in Query:
        name_of_app = Query.replace("open ", "")
        pyautogui.press('win')        
        sleep(1)
        keyboard.write(name_of_app)
        sleep(1)
        keyboard.press('enter')
        sleep(0.5)
        return True
    elif re.search('launch', Query):
                dict_app = {
                    'chrome': 'C:/Program Files/Google/Chrome/Application/chrome'
                }

                app = Query.split(' ', 1)[1]
                path = dict_app.get(app)

                if path is None:
                    Speak('Application path not found')
                    print('Application path not found')

                else:
                    Speak('Launching: ' + app + 'for you sir!')
                    obj.launch_any_app(path_of_app=path)
  
    elif "play my song." in Query:
        os.startfile(r"D:\jarvis\Elley Duhé - MIDDLE OF THE NIGHT (Lyrics)(MP3_320K).mp3")
        return True
    elif "pause youtube" in Query:
        pyautogui.press("k")
        Speak("the video has been pause")
    elif "play youtube" in Query:
        pyautogui.press("k")
        Speak("the video has been start")
    elif "mute youtube" in Query:
        pyautogui.press("m")
        Speak("the video has been mute") 

    elif "close" in Query:
        if "tab" in Query:
            if "all" in Query:
                pyautogui.hotkey("ctrl", "w")
                return True
            else:
                try:
                    num_tabs = int(Query.split()[0])
                    for i in range(num_tabs):
                        pyautogui.hotkey("ctrl", "w")
                    return True
                except ValueError:
                    pass
        else:
            dictapp = {"chrome": "chrome", "firefox": "firefox", "notepad": "notepad", "vscode": "Code","youtube": "youtube" }
            for app in dictapp:
                if app in Query:
                    os.system(f"taskkill /f /im {dictapp[app]}.exe")
                    return True
    
    return False


