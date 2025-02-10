import pyttsx3
import pyautogui
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import os

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 150)

model_path = "vosk-model-en-in-0.5/vosk-model-en-in-0.5"  # Path to your Vosk model

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    """Function to capture voice command and return the query as text"""
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

def photo():
    pyautogui.press("super")
    pyautogui.typewrite("camera")
    pyautogui.press("Enter")
    pyautogui.press("Enter")
    pyautogui.sleep(2)

def screenshot():
    location = ("C:/Users/Rutvik/OneDrive/Desktop/Application Screenshot")
    count = 1
    for filename in os.listdir(location):
        if filename.startswith("ss") and filename.endswith(".jpg"):
            try:
                existing_number = int(filename[2:-4])
                count = max(count, existing_number + 1)
            except ValueError:
                pass
    filename = f"ss{count}.jpg"
    filepath = os.path.join(location, filename)
    im = pyautogui.screenshot()
    im.save(filepath)
    print(f"Screenshot saved as: {filepath}")
    speak(f"Screenshot saved successfully")
