import pyttsx3
import wave
import json
import os
from vosk import Model, KaldiRecognizer
import pyaudio
import datetime 
from datetime import date, time, timedelta
import pyautogui
import pywhatkit

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 150)

model = Model("vosk-model-en-in-0.5")  # Replace with the path to your Vosk model directory

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
                print(f"You said: {query}")
                break

    # Cleaning up resources
    stream.stop_stream()
    stream.close()
    p.terminate()
    return query

def sendMessage():
    # Mapping names to phone numbers
    contacts = {
        "Mom": "+919321057429",   # Add more contacts as needed
        "Dad": "+919004600447",
        "Shubham": "+918169228640",
        "Swayam": "+919152658266",
        "Sushant": "+919152336698",
        "Rishikesh": "+917208198616",
        "Harshal": "+919819223752",
        "Vibha" : "+917977471711",
        "Saniya" : "+917738919893" 
    }

    speak("Who do you want to message?")
    recipient = takeCommand().lower()  # Get recipient name through voice
    phone_number = None

    # Find the corresponding phone number
    for name, number in contacts.items():
        if name.lower() in recipient:
            phone_number = number
            break

    if phone_number:
        speak("What's the message?")
        message = takeCommand()  # Get message content through voice
        try:
            pywhatkit.sendwhatmsg_instantly(phone_number, message)
            print("Message sent successfully.")
            speak("Message sent successfully.")
        except Exception as e:
            print(f"Failed to send message: {e}")
    else:
        print("Contact not found.")
        speak ("Contact not found.")
