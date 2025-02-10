import pyttsx3
import json
import os
from vosk import Model, KaldiRecognizer
import pyaudio

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
engine.setProperty("rate",150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    model = Model("vosk-model-en-in-0.5")
    recognizer = KaldiRecognizer(model, 16000)

    # Setting up audio input
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Listening...")
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            query = result_dict.get("text", "")
            if query:
                print(f"You said: {query}")
                break

    # Cleaning up resources
    stream.stop_stream()
    stream.close()
    p.terminate()
    return query

def shutSystem():
    speak("Are You sure you want to shutdown")
    shutdown = takeCommand()
    if "yes" in shutdown.lower():
        os.system("shutdown /s /t 1")
    elif "no" in shutdown.lower():
        speak("Shutdown canceled.")
    else:
        speak("invalid input. Please say 'yes' or 'no'." )