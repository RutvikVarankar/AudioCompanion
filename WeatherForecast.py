import pyttsx3
import wave
import json
import os
from vosk import Model, KaldiRecognizer
import pyaudio
import wikipedia
import pywhatkit
import webbrowser
import requests
from bs4 import BeautifulSoup

# Initialize Text-to-Speech Engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(text):
    """Function to speak the given text"""
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    """Function to capture voice command and return the query as text"""
    model_path = "vosk-model-en-in-0.5"  # Path to your Vosk model
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

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

    stream.stop_stream()
    stream.close()
    p.terminate()

    return query.lower()

def Temperature(query):
    if "temperature" in query:
        api_key = "a68e1727e5084f299eb104718252701"  # Replace with your actual API key
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q=Mumbai"
        r = requests.get(url)
        data = r.json()

        if "current" in data:
            temp = data["current"]["temp_c"]
            speak(f"Current temperature in Mumbai is {temp} degrees Celsius.")
        else:
            speak("Sorry, couldn't find the temperature information.")

def Weather(query):
    if "weather" in query:
        api_key = "a68e1727e5084f299eb104718252701"  # Replace with your actual API key
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q=Mumbai"
        r = requests.get(url)
        data = r.json()

        if "current" in data:
            weather = data["current"]["condition"]["text"]
            speak(f"Current weather in Mumbai is {weather}.")
        else:
            speak("Sorry, couldn't find the weather information.")
