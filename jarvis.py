import pyttsx3
import datetime 
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice',voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak('Good morning!')
    elif hour>=12 and hour<18:
        speak('Good Afternoon!')
    else:
        speak('Good Evening!')

    speak("I am jarvis sir. Please tell me how may I help you")

def takeCommand():
#we will be gave any Command and jarvis do this.
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        #print(e)
        print("Say that again please...")
        return "None"
    return query


if __name__=="__main__":
    wishMe()
    while True:
        query=takeCommand().lower()

        if "wikipedia" in query:
            speak('Searching wikipedia...')
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("youtube.com")

        elif "open google" in query:
            webbrowser.open("google.co.in")

        elif 'play music' in query:
            music_dir = 'E:\\songs\\panjabi song'
            songs = os.listdir(music_dir)
            #print(songs)
            os.startfile(os.path.join(music_dir,songs[random.randint(1,25)]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'marvel' in query:
            marvel = "E:\\movies\\Marvels"
            os.startfile(marvel)

        elif 'open vlc' in query:
            vlc = "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
            os.startfile(vlc)

        elif "exit" in query:
            exit()
        
