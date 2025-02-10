from fnmatch import translate
from time import sleep
from googletrans import Translator
import googletrans  # pip install googletrans
from gtts import gTTS
from vosk import Model, KaldiRecognizer
import pyttsx3
import os
import json
from playsound import playsound
import pyaudio
import time
import asyncio

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 150)

model = Model("./vosk-model-en-in-0.5")  # Replace with the path to your Vosk model directory

# Function to speak out the input text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user's voice and convert it to text
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

async def translategl(query):
    speak("SURE SIR")
    print(googletrans.LANGUAGES)
    translator = Translator()
    speak("Choose the language in which you want to translate")
    b = input("To_Lang :- ")   
    text_to_translate = await translator.translate(query, src="auto", dest=b)
    text = text_to_translate.text
    try: 
        speakgl = gTTS(text=text, lang=b, slow=False)
        speakgl.save("voice.mp3")
        
        # Check if the audio file was created successfully

        if os.path.exists("voice.mp3"):
            try:
                playsound("voice.mp3")
            except Exception as e:
                print(f"Error playing audio file: {e}")

        else:
            print("Audio file was not created successfully.")
        
        time.sleep(5)
        os.remove("voice.mp3")
    except Exception as e:
        print(f"Unable to translate: {e}")

# Call the translategl function
async def main():
    query = takeCommand()  # Get the user's voice input
    await translategl(query)  # Call the translategl function with the user's input

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
