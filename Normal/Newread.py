import requests
import json
import pyttsx3
import speech_recognition as sr
def Listen():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,0,8) # Listening Mode.....
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language="en")

    except:
        return ""
    
    query = str(query).lower()
    return query

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

def latestnews():
    apidict ={"business":"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=e385fe2aead94553908da9e107b53f79",
     "entertainment" : "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=e385fe2aead94553908da9e107b53f79",
            "health" : "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=e385fe2aead94553908da9e107b53f79",
            "science" :"https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=e385fe2aead94553908da9e107b53f79",
            "sports" :"https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=e385fe2aead94553908da9e107b53f79",
            "technology" :"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=e385fe2aead94553908da9e107b53f79"}
    
    content = None
    url = None
    Speak("Which field news do you want, [business] , [health] , [technology], [sports] , [entertainment] , [science]")
    field = Listen()
    for key ,value in apidict.items():
        if key.lower() in field.lower():
            url = value
            print(url)
            print("url was found")
            break
        else:
            url = True
    if url is True:
        print("url not found")

    news = requests.get(url).text
    news = json.loads(news)
    Speak("Here is the first news.")

    arts = news["articles"]
    for articles in arts :
        article = articles["title"]
        print(article)
        Speak(article)
        news_url = articles["url"]
        print(f"for more info visit: {news_url}")

        a = Listen()
        if str(a) == "okay":
            pass
        elif str(a) == "break":
            break
        
    Speak("thats all")




    
