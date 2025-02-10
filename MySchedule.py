import pyttsx3
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from pygame import mixer
from plyer import notification
import os

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 150)

# Check if the Vosk model path is valid
model_path = "./vosk-model-en-in-0.5"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Vosk model not found at {model_path}")

model = Model(model_path)

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
                query = query.replace("so", "show")
                print(f"You said: {query}")
                return query  # Ensure a valid string is returned
    return ""  # Return an empty string if no valid input is captured

def setSchedule():
    tasks = [] 
    speak("Do you want to clear old tasks (Plz speak YES or NO)")
    query = takeCommand().lower()
    try:
        if "yes" in query:
            with open("tasks.txt", "w") as file:
                file.write("")
            no_tasks = int(input("Enter the no. of tasks :- "))
            for i in range(no_tasks):
                tasks.append(input("Enter the task :- "))
                with open("tasks.txt", "a") as file:
                    file.write(f"{i}. {tasks[i]}\n")
        elif "no" in query:
            no_tasks = int(input("Enter the no. of tasks :- "))
            for i in range(no_tasks):
                tasks.append(input("Enter the task :- "))
                with open("tasks.txt", "a") as file:
                    file.write(f"{i}. {tasks[i]}\n")
    except Exception as e:
        print(f"Error in setting schedule: {e}")

def showSchedule():
    try:
        with open("tasks.txt", "r") as file:
            content = file.read()
        mixer.init()
        mixer.music.load("notification.mp3")
        mixer.music.play()
        notification.notify(
            title="My schedule :-",
            message=content,
            timeout=15
        )
    except Exception as e:
        print(f"Error displaying notification: {e}")
