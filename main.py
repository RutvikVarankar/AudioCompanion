import asyncio
import pyttsx3
import wave
import json
import os
from vosk import Model, KaldiRecognizer
import pyaudio
import datetime 
from datetime import date
import pyautogui
from plyer import notification
from pygame import mixer

from GreetMe import greetMe
from Translator import translategl
from MySchedule import setSchedule
from MySchedule import showSchedule
from FocusMode import enable_focus_mode
from FocusGraph import Graph
from OpenClose import openappweb
from OpenClose import closeappweb
from SearchNow import searchGoogle
from SearchNow import searchYoutube
from SearchNow import searchWikipedia
from WeatherForecast import Temperature
from WeatherForecast import Weather
from playlist import myFavourite
from keyboard import volumeup
from keyboard import volumedown
from Alarm import alarm
from newsRead import latestnews
from Calculator import WolfRamAlpha
from Calculator import Calc
from Whatsapp import sendMessage
from changePass import ChangePassword
from Shutdown import shutSystem
from internet import intSpeed
from camera import photo
from camera import screenshot
from Email import sendEmail

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
engine.setProperty("rate",150)

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
                query = query.replace("dot",".")
                query = query.replace("so","show")
                query = query.replace("set down","shutdown")
                print(f"You said: {query}")
                break

    # Cleaning up resources
    stream.stop_stream()
    stream.close()
    p.terminate()
    return query

for i in range(3):
    speak("Please enter your password")
    a = input("Enter Password to open :- ")
    pw_file = open("password.txt","r")
    pw = pw_file.read()
    pw_file.close()
    if (a==pw):
        print("Hello, I am AudioCompanion. How can I assist you?")
        speak("Hello, I am AudioCompanion. How can I assist you?")
        break
    elif (i==2 and a!=pw):
        exit()
    elif (a!=pw):
        print("Try Again")
        speak("Try Again")

from GUI import play_gif
play_gif

if __name__ == "__main__":
    listening = True

    while True:
        
        query = takeCommand().lower()
        if "enter" in query:
            pyautogui.press("enter")

        if "wake up" in query:
            greetMe()

        elif "translate" in query:
            query = query.replace("translate", "").strip()
            asyncio.run(translategl(query))

        elif "schedule my day" in query or "make my schedule" in query or "today schedule" in query:
            setSchedule()
        elif "show my schedule" in query:
            showSchedule()

        elif "hello" in query:
            speak("Hello sir, how are you ?")
        elif "I am fine" in query:
            speak("that's great sir")
        elif "how are you" in query:
            speak("perfect, sir")
        elif "thank you" in query:
            speak("you are welcome, sir")
        elif "by" in query:
            speak("Bye sir, have a nice day")

        elif "focus mode" in query:
            print("Are you sure that you want to enter focus mode :- [SAY YES OR NO] ")
            speak("Are you sure that you want to enter focus mode :- [SAY YES OR NO] ")
            confirm = takeCommand()
            if "yes" in confirm.lower():
                speak("Entering the focus mode....")
                enable_focus_mode()
            elif "no" in confirm.lower():
                pass
            else:
                speak("invalid input. Please say 'yes' or 'no'." )

        elif "show my focus" in query:
            Graph()

        elif "open" in query:
            openappweb(query)
        elif "close" in query:
            closeappweb(query)

        elif "google" in query:
            searchGoogle(query)
        elif "youtube" in query:
            searchYoutube(query)
        elif "wikipedia" in query:
            searchWikipedia(query)

        elif "temperature" in query:
            Temperature(query)
        elif "weather" in query:
            Weather(query)

        elif "my favourite songs" in query or "play my songs" in query or "start my playlist" in query:
            myFavourite()

        elif "pause" in query:
            pyautogui.press("k")
            speak("video paused")
        elif "play" in query:
            pyautogui.press("k")
            speak("video played")
        elif "mute" in query:
            pyautogui.press("m")
            speak("video muted")
        elif "unmute" in query:
            pyautogui.press("m")
            speak("video muted")

        elif "volume up" in query:
            speak("Turning volume up,sir")
            volumeup()
        elif "volume down" in query:
            speak("Turning volume down, sir")
            volumedown()

        elif "set an alarm" in query:
            print("Input time example :- HH and MM and SS")
            speak("Set the time")
            alarm_time = input("Please tell the time :- ")
            print(alarm_time)
            alarm(alarm_time)
            speak("Done, sir")

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")    
            speak(f"Sir, the current time is {strTime}")
        elif "date" in query:
            today = date.today()   
            formatted_date = today.strftime("%B %d, %Y") 
            speak(f"Sir, Today's date is {formatted_date}")

        elif "remember that" in query:
            rememberMessage = query.replace("remember that","")
            speak("You told me to remember that"+rememberMessage)
            remember = open("Remember.txt","w")
            remember.write(rememberMessage)
            remember.close()
        elif "what do you remember" in query:
            remember = open("Remember.txt","r")
            speak("You told me to remember that" + remember.read())

        elif "news" in query:
            latestnews()

        elif "calculate" in query:
            query = query.replace("calculate","")
            Calc(query)

        elif "whatsapp" in query:
            sendMessage()

        elif "change password" in query:
            ChangePassword()

        elif "shutdown the system" in query or "shut down the system" in query:
            shutSystem()

        elif "internet speed" in query or "show internet speed" in query:
            intSpeed()

        elif "click my photo" in query:
            
            photo()
        elif "screenshot" in query:
            screenshot()

        elif "send email" in query:
            sendEmail()

        elif "finally sleep" in query or "go to sleep" in query:
            speak("Goodbye, Sir")
            exit()
