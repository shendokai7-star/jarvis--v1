import speech_recognition as sr #pip install speechrecognition
from googletrans import Translator #pip install googletrans==3.1.0a0

# 1 - Listen : Hindi or English
def ignore_words(line, ignore_list):
    words = line.split()
    filtered_words = [word for word in words if word not in ignore_list]
    return ' '.join(filtered_words)

def Listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 8) # Listening Mode.....
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="eng-in")
   
    except:
        return ""
    
    query = str(query).lower()
    return query


# 2 - Translation

def TranslationHinToEng(Text):
    line = str(Text)
    translate = Translator()
    result = translate.translate(line)
    data = result.text
    print(f"You : {data} ")
    return data

# 3 - Connect

def MicExecution(ignore_list=["Jarvis","jarvis","Jarved","jarved","jarves","jarved"]):
    query = Listen()
    data = TranslationHinToEng(query)
    data = ignore_words(data, ignore_list)
    print("")
    print(f"You asked : {data} ")
    if "jarvis" not in ignore_list:
        data = data.replace("jarvis", "")
        print("")
        print(f"You asked : {data} ")
    return data

