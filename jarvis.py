import pyttsx3
import datetime 
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random

engine = pyttsx3.init()
#engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice',voices[1].id)


def speak(audio):
    print(f"Jarvis: {audio}")
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception:
        pass

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak('Good morning Pankaj')
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


def find_song_in_folder(folder_path, song_name):
    song_name = song_name.lower().strip()
    if not song_name:
        return None

    for song in os.listdir(folder_path):
        file_name = os.path.splitext(song)[0].lower()
        if song_name == file_name or song_name in file_name or file_name in song_name:
            return os.path.join(folder_path, song)
    return None


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
            webbrowser.open("google.com")

        
        elif 'play music' in query or 'play song' in query:
            music_dir = r'D:\song'

            speak("Which song do you want to play, sir?")
            
            song_name = takeCommand()

            if not song_name or song_name.lower() == 'none':
                speak("No song name received, sir.")
            else:
                song_path = find_song_in_folder(music_dir, song_name)

                if song_path:
                    speak(f"Playing {song_name}, sir.")
                    os.startfile(song_path)
                else:
                    speak("This song is not available, sir.")

        elif 'play baby song' in query:
            music_dir = 'D:\\song\\bubu'
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, random.choice(songs)))
        
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

