
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os

# -------------------- TEXT TO SPEECH --------------------

# Use Windows SAPI5 on Windows
if os.name == "nt":
    engine = pyttsx3.init("sapi5")
else:
    engine = pyttsx3.init()

voices = engine.getProperty("voices")

if voices:
    # Use the second voice if available; otherwise, use the first
    voice_index = 1 if len(voices) > 1 else 0
    engine.setProperty("voice", voices[voice_index].id)

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)


def speak(audio):
    """Speak text and show any text-to-speech errors."""
    message = str(audio)
    print(f"Jarvis: {message}")

    try:
        engine.say(message)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")


# -------------------- GREETING --------------------

def wishMe():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        speak("Good morning, Pankaj.")
    elif 12 <= hour < 18:
        speak("Good afternoon, Pankaj.")
    else:
        speak("Good evening, Pankaj.")

    speak("I am Jarvis, sir. Please tell me how may I help you?")


# -------------------- SPEECH RECOGNITION --------------------

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8


def takeCommand():
    """Listen to the microphone and convert speech to text."""

    try:
        with sr.Microphone() as source:
            print("Listening...")

            # Adjust microphone sensitivity to background noise
            recognizer.adjust_for_ambient_noise(source, duration=0.3)

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        print("Recognizing...")

        query = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print(f"You said: {query}\n")
        return query

    except sr.WaitTimeoutError:
        print("No speech detected.")
        return ""

    except sr.UnknownValueError:
        print("Sorry, I could not understand that.")
        return ""

    except sr.RequestError as e:
        print(f"Speech recognition service error: {e}")
        speak("Sorry sir, I am having trouble connecting to the speech service.")
        return ""

    except (OSError, AttributeError) as e:
        print(f"Microphone error: {e}")
        speak("Sorry sir, I could not access the microphone.")
        return ""


# -------------------- FIND SONG --------------------

MUSIC_DIR = r"D:\song"

AUDIO_EXTENSIONS = (
    ".mp3",
    ".wav",
    ".m4a",
    ".flac",
    ".aac",
    ".wma",
    ".ogg"
)


def find_song_in_folder(folder_path, song_name):
    """Find a song by its filename, ignoring case and extension."""

    if not os.path.isdir(folder_path):
        print(f"Music folder does not exist: {folder_path}")
        return None

    song_name = song_name.strip().casefold()

    if not song_name:
        return None

    try:
        files = [
            file for file in os.listdir(folder_path)
            if file.lower().endswith(AUDIO_EXTENSIONS)
            and os.path.isfile(os.path.join(folder_path, file))
        ]
    except OSError as e:
        print(f"Could not read music folder: {e}")
        return None

    # First, search for an exact filename match
    for file in files:
        file_name = os.path.splitext(file)[0].casefold()

        if song_name == file_name:
            return os.path.join(folder_path, file)

    # Next, search for a partial filename match
    for file in files:
        file_name = os.path.splitext(file)[0].casefold()

        if len(song_name) >= 3 and (
            song_name in file_name or file_name in song_name
        ):
            return os.path.join(folder_path, file)

    return None


# -------------------- MAIN PROGRAM --------------------

if __name__ == "__main__":

    wishMe()

    while True:

        query = takeCommand().strip().casefold()

        # Ignore empty or unrecognized commands
        if not query:
            continue

        # Wikipedia search
        if "wikipedia" in query:
            search_query = query.replace("wikipedia", "").strip()

            if not search_query:
                speak("Please tell me what you want to search on Wikipedia.")
                continue

            try:
                speak("Searching Wikipedia, sir.")

                results = wikipedia.summary(
                    search_query,
                    sentences=2
                )

                print(results)
                speak("According to Wikipedia.")
                speak(results)

            except Exception as e:
                print(f"Wikipedia error: {e}")
                speak("Sorry sir, I could not find that information.")

        # Open YouTube
        elif "open youtube" in query:
            speak("Opening YouTube, sir.")
            webbrowser.open("https://www.youtube.com")

        # Open Google
        elif "open google" in query:
            speak("Opening Google, sir.")
            webbrowser.open("https://www.google.com")

        # Play music
        elif any(command in query for command in (
            "play music",
            "play song",
            "play a song",
            "play some music"
        )):

            if not os.path.isdir(MUSIC_DIR):
                speak("Sorry sir, I could not find your music folder.")
                print(f"Please check this folder: {MUSIC_DIR}")
                continue

            # Speak the question BEFORE opening the microphone
            speak("Which song do you want to play, sir?")

            # Now listen for the song name
            song_name = takeCommand().strip()

            if not song_name:
                speak("Sorry sir, I did not receive the song name.")
                continue

            song_path = find_song_in_folder(
                MUSIC_DIR,
                song_name
            )

            if song_path:
                try:
                    speak(f"Playing {song_name}, sir.")
                    os.startfile(song_path)

                except OSError as e:
                    print(f"Could not open song: {e}")
                    speak("Sorry sir, I could not open this song.")

            else:
                speak(
                    f"Sorry sir, {song_name} is not available "
                    "in your music folder."
                )

        # Tell the time
        elif "the time" in query or query == "time":
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir, the time is {current_time}.")

        # Exit Jarvis
        elif "exit" in query or "shutdown jarvis" in query:
            speak("Goodbye, Pankaj. Have a nice day!")
            break

        else:
            print("No matching command found.")
