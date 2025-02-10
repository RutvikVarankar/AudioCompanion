import pyttsx3
import json
from vosk import Model, KaldiRecognizer
import pyaudio
import wikipedia
import pywhatkit
import webbrowser

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

def searchGoogle(query):
    """Function to search Google using the query"""
    if "google" in query:
        query = query.replace("google search", "")
        query = query.replace("google", "")
        query = query.strip()
        speak("This is what I found on Google")

        try:
            pywhatkit.search(query)
            try:
                result = wikipedia.summary(query, sentences=1)
                speak(result)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("The query is ambiguous, please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("No Wikipedia page found for the query.")
            webbrowser.open(f"https://www.google.com/search?q={query}")

        except Exception as e:
            speak("I couldn't perform the search, but I've opened the search in your browser.")
            webbrowser.open(f"https://www.google.com/search?q={query}")

def searchYoutube(query):
    if "youtube" in query:
        speak("This is what I found for your search!") 
        query = query.replace("youtube search", "")
        query = query.replace("youtube", "")
        query = query.replace("you tube", "")
        query = query.strip()
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        speak("Opening YouTube...")
        pywhatkit.playonyt(query)
        speak("Done, Sir")
    else:
        speak("I didn't find a YouTube-related command in your query.")

def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching from wikipedia....")
        query = query.replace("wikipedia","")
        query = query.replace("search wikipedia","")
        query = query.strip()
        results = wikipedia.summary(query, sentences=2)
        print(results)
        speak(results)