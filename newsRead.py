import requests
import json
import pyttsx3
import pyaudio
from vosk import Model, KaldiRecognizer

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

model = Model("vosk-model-en-in-0.5")  # Replace with the path to your Vosk model directory

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():  
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
                query = query.replace("dot", ".")
                print(f"You said: {query}")
                break

    # Cleaning up resources
    stream.stop_stream()
    stream.close()
    p.terminate()
    return query

def latestnews():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=ae4a9fdd5671442cb5815f0ec81dbcf2"  # World News API URL

    speak("Fetching the latest news...")
    response = requests.get(url)
    news = response.json()  # Get the JSON response

    if 'articles' not in news:
        print("Error fetching news:", news)  # Print the entire response for debugging
        speak("Sorry, I couldn't fetch the news at this time.")
        return

    speak("Here is the first news.")
    arts = news["articles"]
    for articles in arts:
        article = articles["title"]
        print(article)
        speak(article)
        news_url = articles["url"]
        print(f"For more info visit: {news_url}")

        speak("[Speak continue to continue] and [speak stop to stop]")
        consent = takeCommand().lower()  # Corrected to call lower() method
        if "continue" in consent:
            pass
        elif "stop" in consent:
            break

    speak("That's all for now.")
