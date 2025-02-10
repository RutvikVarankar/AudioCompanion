import os
import pyautogui
import webbrowser
import pyttsx3
from time import sleep
import re

# Initialize Text-to-Speech Engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(text):
    """Function to speak the given text"""
    engine.say(text)
    engine.runAndWait()

def openappweb(query):
    query = query.replace("open","")
    pyautogui.press("super")
    pyautogui.typewrite(query)
    pyautogui.press("Enter")  
    pyautogui.press("Enter")  

def closeappweb(query):
    speak("Closing, sir")
    if "close application" in query:
        pyautogui.hotkey("alt", "f4")  # Updated line
    elif "close tab" in query or "1 tab" in query:
        pyautogui.hotkey("ctrl", "w")
        speak("one tab closed")
