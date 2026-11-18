import speech_recognition as sr
from dotenv import load_dotenv
import os 
import webbrowser
import musicLibrary
import requests
import pyttsx3
import threading
import time
import pythoncom
import ollama

load_dotenv()
speech_lock=threading.Lock()
recognizer= sr.Recognizer()
newsapi=os.getenv("NEWS_API_KEY")

def speak(text):
    with speech_lock:
        pythoncom.CoInitialize()
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        print("Jarvis:", text)

def aiProcess(command):       
    response=ollama.chat(
        model='llama3',
        messages=[
            {'role':'system','content':'you are a virtual assistant named jarvis skilled in '
            'general tasks like alexa and you should give brief answers.'},
            {'role':'user','content':command}
            ]
    )
    return response['message']['content']
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open upwork" in c.lower():
        webbrowser.open("https://upwork.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")            
    elif "open telegram" in c.lower():
        webbrowser.open("https://telegram.com")
    elif "open pinterest" in c.lower():
        webbrowser.open("https://pinterest.com")

    elif c.lower().startswith("play"):
        song=c.lower().replace("play","",1).strip().replace(" ","-")
        link=musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower(): 

        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}") 
        if r.status_code==200:
            data=r.json()
            articles=data.get('articles',[])
            for article in articles:
                speak(article['title'])

    else: #let Ollama respond to this
        output=aiProcess(c) 
        speak(output)
                    

if __name__ == "__main__":
    speak("initializing jarvis")

    while True:
        # listen for the wake word "jarvis"
        # obtain audio from the microphone
        r= sr.Recognizer()
       
        print("recognizing...")

        try:
            with sr.Microphone() as source:
                print("listening...")
                audio=r.listen(source,timeout=6,phrase_time_limit=3)

            word=r.recognize_google(audio)
            if (word.lower()=="jarvis"):
                time.sleep(1)
                speak("Yaa")
                # listen for command
                with sr.Microphone() as source:
                    audio=r.listen(source)
                    command = r.recognize_google(audio)
                    print("python heard:",command)
                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))        