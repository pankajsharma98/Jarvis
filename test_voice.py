
import pyttsx3

engine = pyttsx3.init("sapi5")

voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

engine.say("Good evening, Pankaj.")
engine.runAndWait()

engine.say("I am Jarvis, sir. Please tell me how may I help you.")
engine.runAndWait()

engine.say("Which song do you want to play, sir.")
engine.runAndWait()
