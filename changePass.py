import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
engine.setProperty("rate",150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ChangePassword():
    speak("What's the new password")
    new_pw = input("Enter the new password\n")
    new_password = open("password.txt","w")
    new_password.write(new_pw)
    new_password.close()
    speak("Done sir")
    speak(f"Your new password is{new_pw}")
            